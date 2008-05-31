%{!?python_sitelib: %define python_sitelib %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib()")}

Name: python-routes
Version: 1.8
Release: 2%{?dist}
Summary: Rails-like routes for Python

Group: Development/Languages
License: BSD
URL: http://routes.groovie.org/
Source0: http://pypi.python.org/packages/source/R/Routes/Routes-%{version}.tar.gz
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch: noarch
BuildRequires: python-setuptools-devel


%description
Routes is a Python re-implementation of the Rails routes system for mapping
URL's to Controllers/Actions and generating URL's. Routes makes it easy to
create pretty and concise URL's that are RESTful with little effort.


%prep
%setup -q -n Routes-%{version}


%build
%{__python} setup.py build


%install
rm -rf $RPM_BUILD_ROOT
%{__python} setup.py install -O1 --skip-build --root $RPM_BUILD_ROOT


%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr(-,root,root,-)
%doc INSTALL LICENSE README docs
%{python_sitelib}/*


%changelog
* Sun May 11 2008 Kyle VanderBeek <kylev@kylev.com> - 1.8-2
- Fix rpmlint warning.
- Add documentation files.

* Wed Apr  9 2008 Kyle VanderBeek <kylev@kylev.com> - 1.8-1
- Initial version.

