Summary:	Vserver Name Service Switch Module
Name:		nss_vserver
Version:	0
Release:	0.1
License:	public domain
Group:		Base
Source0:	http://dev.call2ru.com/%{name}.tar.bz2
# Source0-md5:	c1069fefb23b4bb699b857ea1062d75a
Patch0:		%{name}-make.patch
URL:		http://linux-vserver.org/HowtoHostAuth
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_libdir		/%{_lib}

%description
This is host-auth module for linux-vserver powered systems.

nss_vserver module allows you to auth users from vservers on host via
standard PAM auth. If you want to make user login into their vserver
via host, you should also get a bit modified vslogin (originally
written by Alec Thomas, <http://swapoff.org/LinuxVServer>) from
<http://linux-vserver.org/HowtoHostAuth>.

%prep
%setup -q -n %{name}
%patch0 -p1

%build
%{__make} CC="%{__cc}" DBG="%{rpmcflags}"

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_libdir}
install libnss_vserver.so.* $RPM_BUILD_ROOT%{_libdir}

%clean
rm -rf $RPM_BUILD_ROOT

%post   -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc COPYING README
%attr(755,root,root) %{_libdir}/*.so*
