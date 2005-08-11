#
#  base
#
#  Created by Ben Bangert on 2005-08-08.
#  Copyright (c) 2005 Parachute. All rights reserved.
#

import re, time, sys
from urllib import quote_plus

def quote(string):
    return quote_plus(str(string), '/')

if sys.version < '2.4':
    from sets import ImmutableSet as frozenset

class Route(object):
    """
    The Route object holds a route recognition and generation routine, typical usage looks like:
    
    newroute = Route(':controller/:action/:id')
    newroute = Route('date/:year/:month/:day', controller="blog", action="view")
    
    Note: Route is generally never called directly, a Mapper instances connect method should
    be used to add routes.
    
    """
    
    def __init__(self, routepath, **kargs):
        """
        Initialize a route, with a given routepath for matching/generation, and a set of keyword
        args that setup defaults.
        """
        
        reserved_keys = ['requirements']
        
        # Build 3 lists, our route list, the default keys, and the route keys
        routelist = routepath.split('/')
        defaultkeys = frozenset([key for key in kargs.keys() if key not in reserved_keys])
        routekeys = frozenset([key[1:] for key in routelist if (key.startswith(':') or key.startswith('*')) and key not in reserved_keys])
        
        maxkeys = defaultkeys | routekeys
        # Save our routelist
        self.routelist = routelist[:]
        self.routepath = routepath
        
        # Build a req list with all the regexp requirements for our args
        self.reqs = kargs.has_key('requirements') and kargs['requirements']
        if not self.reqs: self.reqs = {}
        
        # Put together our list of defaults, stringify non-None values
        # and add in our action/id default if they use it and didn't specify it
        defaults = {}
        for key in defaultkeys:
            if kargs[key] != None:
                defaults[key] = str(kargs[key])
            else:
                defaults[key] = None
        if 'action' in routekeys and not defaults.has_key('action'):
            defaults['action'] = 'index'
        elif not defaults.has_key('action') and 'controller' in maxkeys:
            defaults['action'] = 'index'
        if 'id' in routekeys and not defaults.has_key('id'):
            defaults['id'] = None
        defaultkeys = frozenset([key for key in defaults.keys() if key not in reserved_keys])

        # Save the maximum keys we could utilize
        self.maxkeys = defaultkeys | routekeys

        # We walk our route backwards, anytime we can leave off a key due to it
        # having a default, or being None, we know its not needed. As soon as we
        # add something though, the rest is needed no matter what.
        minkeys = []
        backcheck = routelist[:]
        gaps = False
        backcheck.reverse()
        self.routebackwards = backcheck[:]
        for part in backcheck:
            if not part.startswith(':'):
                gaps = True
                continue
            key = part[1:]
            if defaults.has_key(key) and not gaps:
                continue
            minkeys.append(key)
            gaps = True
        self.minkeys = frozenset(minkeys)

        # Our hardcoded args exist as defaults, but have no place in the route to
        # specify them. Thus for the route to be generated, the args passed in must
        # match these ones for the URL to be usable.
        hardcoded = []
        for key in self.maxkeys:
            if key not in routekeys and defaults[key] is not None:
                hardcoded.append(key)
        self.defaults = defaults
        self.hardcoded = frozenset(hardcoded)
    
    def makeregexp(self, clist):
        """
        Create a regular expression for matching purposes, this MUST be called before match
        can function properly.
        
        clist should be a list of valid controller strings that can be matched, for this reason
        makeregexp should be called by the web framework after it knows all available controllers
        that can be utilized
        """
        
        (reg, noreqs, allblank) = self.buildnextreg(self.routelist, clist)
        
        if not reg: reg = '/'
        reg = '^' + reg + '$'
        #print "\nRegexp Made: " + reg
        
        self.regexp = reg
        self.regmatch = re.compile(reg)
        
    def buildnextreg(self, path, clist):
        part = path[0]
        reg = ''
        
        # noreqs will remember whether the remainder has either a string match, or a non-defaulted
        # regexp match on a key
        (rest, noreqs, allblank) = ('', True, True)
        if len(path[1:]) > 0:
            (rest, noreqs, allblank) = self.buildnextreg(path[1:], clist)
            
        if part.startswith(':'):
            var = part[1:]
            partreg = ''
            
            # First we plug in the proper part matcher
            if self.reqs.has_key(var):
                partreg = '(?P<' + var + '>' + self.reqs[var] + ')'
            elif var == 'controller':
                partreg = '(?P<' + var + '>' + '|'.join(clist) + ')'
            else:
                partreg = '(?P<' + var + '>[^/]+)'
                
            # Now we determine if its optional, or required. This changes depending on what is in
            # the rest of the match. If noreqs is true, then its possible the entire thing is optional
            # as there's no reqs or string matches. If false, then this section isn't optional to complete
            # the match, so we're required no matter what
            if self.reqs.has_key(var): noreqs = False
            if noreqs:
                # The rest is optional, but now we have an optional with a regexp. Wrap to ensure that if we match
                # anything, we match our regexp first
                if self.reqs.has_key(var) and self.defaults.has_key(var):
                    reg = '(/' + partreg + rest + ')?'
                # Or we have a regexp match with no default
                elif self.reqs.has_key(var):
                    allblank = False
                    reg = '(/' + partreg + ')' + rest
                # Or we have a default with no regexp
                elif self.defaults.has_key(var):
                    reg = '(/' + partreg + ')?' + rest
                else:
                    allblank = False
                    reg = '(/' + partreg + ')' + rest
            # In this case, we have something dangling that might need to be matched
            else:
                # If they can all be blank, we can optionally match here, unless we have
                # our own reqs, in which case we're optional match, but MUST match here
                # if we match at all
                if allblank and self.defaults.has_key(var):
                    reg = '(/' + partreg + rest + ')?'
                else:
                    reg = '/' + partreg + rest
        elif part.startswith('*'):
            var = part[1:]
            reg = '(/' + '(?P<' + var + '>.*))*' + rest
        else:
            noreqs = False
            allblank = False
            reg = '/' + part + rest
        return (reg, noreqs, allblank)
        
    def match(self, url):
        """
        Match a url to our regexp. While the regexp might match, this operation isn't
        guaranteed as there's other factors that can cause a match to fail even though
        the regexp succeeds (Default that was relied on wasn't given, requirement regexp
        doesn't pass, etc.).
        
        Therefore the calling function shouldn't assume this will return a valid dict, the
        other possible return is False if a match doesn't work out.
        """
        
        m = self.regmatch.match(url)
        if m:
            matchdict = m.groupdict()
            result = {}
            extras = frozenset(self.defaults.keys()) - frozenset(matchdict.keys())
            for key in self.reqs.keys():
                if key not in matchdict.keys() or matchdict[key] is None:
                    try:
                        print 'Checking default for: ' + str(key)
                        result[key] = self.defaults[key]
                    except:
                        return False
                else:
                    value = matchdict[key] or (self.defaults.has_key(key) and self.defaults[key]) or ''
                    if not re.compile('^' + self.reqs[key] + '$').match(value):
                        print "Didn't match reqs"
                        return False
            for key,val in matchdict.iteritems():
                if not val and self.defaults.has_key(key) and self.defaults[key]:
                    result[key] = self.defaults[key]
                else:
                    result[key] = val
            for key in extras:
                result[key] = self.defaults[key]
            return result
        else:
            return False
    
    def generate(self,**kargs):
        """
        Generate a URL from ourself given a set of keyword arguments, toss an exception if this
        set of keywords would cause a gap in the url.
        """
        
        # Verify that our args pass any regexp requirements
        for key in self.reqs.keys():
            if kargs.has_key(key):
                if self.defaults.has_key(key) and self.defaults[key] is None and kargs[key] is None:
                    continue
                if not re.compile('^' + self.reqs[key] + '$').match(str(kargs[key])):
                    raise Exception, "Route doesn't match reqs"

        routelist = self.routebackwards
        urllist = []
        gaps = False
        for part in routelist:
            if part.startswith(':'):
                arg = part[1:]
                if self.defaults.has_key(arg) and kargs.has_key(arg) and str(kargs[arg]) == self.defaults[arg] and not gaps:
                    continue
                if self.defaults.has_key(arg) and not kargs.has_key(arg) and not gaps:
                    continue
                val = kargs.has_key(arg) and kargs[arg]
                if not val:
                    val = self.defaults.has_key(arg) and self.defaults[arg]
                if (not val or val is None) and not gaps:
                    continue
                if val is None:
                    raise Exception, "Route causes gaps"
                val = quote(val)
                urllist.append(val)
                if kargs.has_key(arg): del kargs[arg]
                gaps = True
            elif part.startswith('*'):
                arg = part[1:]
                if kargs.has_key(arg) and kargs[arg] is not None:
                    val = quote(kargs[arg])
                    urllist.append(val)
                    gaps = True
            else:
                gaps = True
                urllist.append(part)
        urllist.reverse()
        url = '/' + '/'.join(urllist)
        extras = frozenset(kargs.keys()) - self.maxkeys
        if extras:
            url += '?'
            url += '&'.join([quote(key)+'='+quote(kargs[key]) for key in extras if key != 'action' or key != 'controller'])
        return url
    

class Mapper(object):
    """
    Instantiate a new mapper and assign a default route:
    m = Mapper()
    m.connect(':controller/:action/:id')
    m.connect('', controller='welcome')
        
    To create URL -> dict translations, all controllers should be scanned, loaded into a list, and
    passed into create_reg() to tell all the routes to generate regexp's used for recognition.
        
    Dict -> URL translation can be done at any point with a mapper by using the generate() method.
    """
    
    def __init__(self):
        """
        Create a new Mapper object and initialize our defaults
        """
        self.matchlist = []
        self.maxkeys = {}
        self.minkeys = {}
        self.cachematch = {}
        self.created_regs = False
        self.urlcache = None
    
    def connect(self, *args, **kargs):
        """
        Create and connect a new route to our Mapper instance. 
            
        The arguments and syntax accepted is identical to the Route creation.
        """
        route = Route(*args, **kargs)
        self.matchlist.append(route)
        exists = False
        for key in self.maxkeys:
            if key == route.maxkeys:
                self.maxkeys[key].append(route)
                exists = True
                break
        if not exists:
            self.maxkeys[route.maxkeys] = [route]
    
    def create_regs(self, clist):
        """
        Iterate through all connected Routes with our controller list (clist), and
        generate regexp's for every route.
        """
        for key,val in self.maxkeys.iteritems():
            for route in val:
                route.makeregexp(clist)
        self.created_regs = True
    
    def match(self, url):
        """
        Match a URL against against one of the routes contained.
        
        Will return None if no valid match is found.
        
        resultdict = m.match('/joe/sixpack')
        """
        if not self.created_regs:
            raise Exception, "Must created regexps first"
            
        for route in self.matchlist:
            match = route.match(url)
            if match: return match
        return None
    
    def generate(self, **kargs):
        """
        Generate a route from a set of keywords and return the url text, or None if no
        URL could be generated.
        
        m.generate(controller='content',action='view',id=10)
        """
        
        # Check the url cache to see if it exists, use it if it does
        if self.urlcache:
            try:
                return urlcache[str(kargs)]
            except:
                pass
        
        keys = frozenset(kargs.keys())
        
        # This keysort is probably expensive, so we'll cache the results. Since key lookups
        # by set isn't the quickest, I try and fetch first, and deal with it when it fails,
        # rather than using has_key then fetching it (two key lookups)
        try:
            keylist = self.cachematch[keys]
        except:
            keylist = self.maxkeys.keys()
            def keysort(a, b):
                # First, if a matches exactly, use it
                if len(keys^a) == 0:
                    return -1
                    
                # Or b matches exactly, use it
                if len(keys^b) == 0:
                    return 1
                    
                # Neither matches exactly, but if they both have just as much in common
                if len(keys&b) == len(keys&a):
                    return cmp(len(a),len(b))     # Then we return the shortest of the two
                
                # Otherwise, we return the one that has the most in common
                else:
                    return cmp(len(keys&b), len(keys&a))
            
            keylist.sort(keysort)
            self.cachematch[keys] = keylist
        
        #print keylist
        for routelist in keylist:
            for route in self.maxkeys[routelist]:
                if len(route.minkeys-keys) != 0: continue
                fail = False
                for key in route.hardcoded:
                    if not kargs.has_key(key):
                        continue
                    if kargs[key] != route.defaults[key]:
                        fail = True
                        break
                if fail: continue
                if len(route.minkeys-keys) == 0:
                    try:
                        path = route.generate(**kargs)
                        if self.urlcache:
                            self.urlcache[str(kargs)] = path
                        return path
                    except:
                        continue
        return None
    

if __name__ == '__main__':
    pass
else:
    m = Mapper()
    m.connect('date/:year/:month/:day', controller = 'blog', action = 'by_date', month = None, day = None)
    m.connect(':controller/:action/:id', id = None)
    url = '/date/2004/20/4'
    c = Mapper()
    c.connect(':controller/:action/:id')

    def bench_gen():
        n = 1000
        start = time.time()
        for x in range(1,n):
            c.generate(controller='content', action='index')
            c.generate(controller='content', action='list')
            c.generate(controller='content', action='show', id='10')
            
            c.generate(controller='admin/user', action='index')
            c.generate(controller='admin/user', action='list')
            c.generate(controller='admin/user', action='show', id='10')
        end = time.time()
        ts = time.time()
        for x in range(1,n*3):
            pass
        en = time.time()
        total = end-start-(en-ts)
        per_url = total / (n*6)
        print "Generation\n"
        print "%s ms/url" % (per_url*1000)
        print "%s urls/s\n" % (1.00/per_url)
    
    def bench_rec():
        n = 1000
        c = Mapper()
        c.connect(':controller/:action/:id')
        c.create_regs(['content','admin/user'])
        start = time.time()
        for x in range(1,n):
            a = c.match('/content')
            a = c.match('/content/list')
            a = c.match('/content/show/10')
            
            a = c.match('/admin/user')
            a = c.match('/admin/user/list')
            a = c.match('/admin/user/show/bbangert')
            
            a = c.match('/admin/user/show/bbangert/dude')
            a = c.match('/admin/why/show/bbangert')
            a = c.match('/content/show/10/20')
            a = c.match('/food')
        end = time.time()
        ts = time.time()
        for x in range(1,n):
            pass
        en = time.time()
        total = end-start-(en-ts)
        per_url = total / (n*10)
        print "Recognition\n"
        print "%s ms/url" % (per_url*1000)
        print "%s urls/s\n" % (1.00/per_url)
    
