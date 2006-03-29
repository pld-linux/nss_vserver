# NOTE
# - we don't need vserver gid if vserver is enabled in
#   /etc/nsswitch.conf, but it's probably sysadmin decision to enable
#   it, so we provide another one in passwd db.
# TODO
# - gid is hardcoded in nss_vserver
%define	vserver_gid 9999
Summary:	Vserver Name Service Switch Module
Name:		nss_vserver
Version:	0
Release:	0.3
License:	public domain
Group:		Base
Source0:	http://dev.call2ru.com/%{name}.tar.bz2
# Source0-md5:	c1069fefb23b4bb699b857ea1062d75a
Patch0:		%{name}-make.patch
URL:		http://linux-vserver.org/HowtoHostAuth
Requires(postun):	/sbin/ldconfig
Requires(postun):	/usr/sbin/groupdel
Requires(pre):	/usr/bin/getgid
Requires(pre):	/usr/sbin/groupadd
Provides:	group(vserver)
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
# FIXME: ldconfig has nothing to do with such soname
install libnss_vserver.so.* $RPM_BUILD_ROOT%{_libdir}

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig

%pre
%groupadd -g %{vserver_gid} vserver

%postun
/sbin/ldconfig
if [ "$1" = "0" ]; then
	%groupremove vserver
fi

%files
%defattr(644,root,root,755)
%doc COPYING README
%attr(755,root,root) %{_libdir}/*.so*
