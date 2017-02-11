%if 0%{?rhel} && 0%{?rhel} <= 7
%global with_python3 0
%else
%global with_python3 1
%endif

Name: python-routes
Version: 2.2
Release: 5%{?dist}
Summary: Rails-like routes for Python

Group: Development/Languages
License: BSD
URL: http://routes.groovie.org/
Source0: http://pypi.python.org/packages/source/R/Routes/Routes-%{version}.tar.gz
BuildArch: noarch
BuildRequires: python-setuptools
BuildRequires: python-nose
BuildRequires: python-webtest
BuildRequires: python-paste
BuildRequires: python-repoze-lru
BuildRequires: python-six
BuildRequires: python-devel

%if 0%{?with_python3}
BuildRequires: python3-devel
BuildRequires: python3-setuptools
BuildRequires: python3-nose
BuildRequires: python3-webtest
BuildRequires: python3-paste
BuildRequires: python3-repoze-lru
BuildRequires: python3-six
%endif

Requires: python-repoze-lru
Requires: python-six

Provides: python2-routes


%description
Routes is a Python re-implementation of the Rails routes system for mapping
URL's to Controllers/Actions and generating URL's. Routes makes it easy to
create pretty and concise URL's that are RESTful with little effort.

This package contains the module built for python2.

%if 0%{?with_python3}
%package -n python3-routes
Summary: Rails-like routes for Python3
Requires: python3-repoze-lru
Requires: python3-six

%description -n python3-routes
Routes is a Python re-implementation of the Rails routes system for mapping
URL's to Controllers/Actions and generating URL's. Routes makes it easy to
create pretty and concise URL's that are RESTful with little effort.

This package contains the module built for python3.

%endif

%prep
%setup -q -n Routes-%{version}

%if 0%{?with_python3}
rm -rf %{py3dir}
cp -a . %{py3dir}
%endif # with_python3


%build
%{__python2} setup.py build

%if 0%{?with_python3}
pushd %{py3dir}
%{__python3} setup.py build
popd
%endif # with_python3


%install
%{__python2} setup.py install --skip-build --root=%{buildroot}

%if 0%{?with_python3}
pushd %{py3dir}
%{__python3} setup.py install --skip-build --root=%{buildroot}
popd
%endif # with_python3


%check
PYTHONPATH=$(pwd) nosetests

%if 0%{?with_python3}
pushd %{py3dir}
PYTHONPATH=$(pwd) nosetests-%{python3_version}
popd
%endif


%files
%defattr(-,root,root,-)
%{!?_licensedir:%global license %%doc}
%license LICENSE.txt
%doc README.rst CHANGELOG.rst docs
%{python2_sitelib}/*

%if 0%{?with_python3}
%files -n python3-routes
%license LICENSE.txt
%doc README.rst CHANGELOG.rst docs
%{python3_sitelib}/*
%endif


%changelog
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

