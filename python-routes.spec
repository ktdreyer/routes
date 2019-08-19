Name: python-routes
Version: 2.4.1
Release: 11%{?dist}
Summary: Rails-like routes for Python

License: BSD
URL: http://routes.groovie.org/
Source0: https://pypi.io/packages/source/R/Routes/Routes-%{version}.tar.gz
BuildArch: noarch

BuildRequires: python3-devel
BuildRequires: python3-setuptools
BuildRequires: python3-nose
BuildRequires: python3-webtest
BuildRequires: python3-paste
BuildRequires: python3-repoze-lru
BuildRequires: python3-six


%global _description\
Routes is a Python re-implementation of the Rails routes system for mapping\
URL's to Controllers/Actions and generating URL's. Routes makes it easy to\
create pretty and concise URL's that are RESTful with little effort.\
\
This package contains the module built for python2.

%description %_description

%package -n python3-routes
Summary: Rails-like routes for Python3
Requires: python3-repoze-lru
Requires: python3-six
%{?python_provide:%python_provide python3-routes}

%description -n python3-routes
Routes is a Python re-implementation of the Rails routes system for mapping
URL's to Controllers/Actions and generating URL's. Routes makes it easy to
create pretty and concise URL's that are RESTful with little effort.

This package contains the module built for python3.


%prep
%setup -q -n Routes-%{version}


%build
%py3_build


%install
%py3_install


%check
PYTHONPATH=$(pwd) nosetests-%{python3_version}


%files -n python3-routes
%license LICENSE.txt
%doc README.rst CHANGELOG.rst docs
%{python3_sitelib}/*


%changelog
* Mon Aug 19 2019 Miro Hrončok <mhroncok@redhat.com> - 2.4.1-11
- Rebuilt for Python 3.8

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2.4.1-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Wed Jul 24 2019 Miro Hrončok <mhroncok@redhat.com> - 2.4.1-9
- Subpackage python2-routes has been removed
  See https://fedoraproject.org/wiki/Changes/Mass_Python_2_Package_Removal

* Sat Feb 02 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2.4.1-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Sat Jul 14 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2.4.1-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Tue Jun 19 2018 Miro Hrončok <mhroncok@redhat.com> - 2.4.1-6
- Rebuilt for Python 3.7

* Wed Feb 28 2018 Iryna Shcherbina <ishcherb@redhat.com> - 2.4.1-5
- Update Python 2 dependency declarations to new packaging standards
  (See https://fedoraproject.org/wiki/FinalizingFedoraSwitchtoPython3)

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2.4.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Sat Aug 19 2017 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 2.4.1-3
- Python 2 binary package renamed to python2-routes
  See https://fedoraproject.org/wiki/FinalizingFedoraSwitchtoPython3

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.4.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Thu May 18 2017 Alan Pevec <alan.pevec@redhat.com> 2.4.1-1
- Update to 2.4.1

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.2-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Mon Dec 19 2016 Miro Hrončok <mhroncok@redhat.com> - 2.2-4
- Rebuild for Python 3.6

* Tue Jul 19 2016 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.2-3
- https://fedoraproject.org/wiki/Changes/Automatic_Provides_for_Python_RPM_Packages

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 2.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Wed Jan  6 2016 Toshio Kuratomi <toshio@fedoraproject.org> - - 2.2-1
- Update to 2.2 and include a python3 subpackage

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.13-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.13-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.13-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Tue Mar 12 2013 Matthias Runge <P@draigBrady.com> - 1.13-2
- Add dependency on python-repoze-lru (new in 1.13)

* Tue Feb 26 2013 Matthias Runge <mrunge@redhat.com> - 1.13-1
- update to 1.13 (rhbz#803019)

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.12.3-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.12.3-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.12.3-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.12.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Tue Oct 05 2010 Luke Macken <lmacken@redhat.com> - 1.12.3-1
- Update to 1.12.3

* Thu Jul 22 2010 David Malcolm <dmalcolm@redhat.com> - 1.12.1-2
- Rebuilt for https://fedoraproject.org/wiki/Features/Python_2.7/MassRebuild

* Wed May 05 2010 Luke Macken <lmacken@redhat.com> - 1.12.1-1
- Update to 1.12.1

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.10.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Sun May 31 2009 Luke Macken <lmacken@redhat.com> - 1.10.3-1
- Update to 1.10.3

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.10.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Tue Jan 06 2009 Luke Macken <lmacken@redhat.com> - 1.10.1-2
- Update to 1.10.1
- Run the test suite

* Sat Nov 29 2008 Ignacio Vazquez-Abrams <ivazqueznet+rpm@gmail.com> - 1.8-3
- Rebuild for Python 2.6

* Sun May 11 2008 Kyle VanderBeek <kylev@kylev.com> - 1.8-2
- Fix rpmlint warning.
- Add documentation files.

* Wed Apr  9 2008 Kyle VanderBeek <kylev@kylev.com> - 1.8-1
- Initial version.

