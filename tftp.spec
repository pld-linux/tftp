Summary:	Client and daemon for the trivial file transfer protocol (tftp)
Summary(pl):	Klient i demon tftp (trivial file transfer protocol)
Name:		tftp
Version:	0.10
Release:	5
Copyright:	BSD
Group:		Networking
Source:		ftp://sunsite.unc.edu/pub/Linux/system/network/file-transfer/netkit-%{name}-%{version}.tar.gz
Source1:	tftpd.inetd
Patch:		%{name}-%{version}-misc.patch
Patch1:		%{name}-%{version}-security.patch
Requires:	inetdaemon
Requires:	rc-inetd
BuildRoot:	/tmp/%{name}-%{version}-root

%description
The trivial file transfer protocol (tftp) is normally used only for 
booting diskless workstations. It provides very little security, and
should not be enabled unless it is needed. The tftp server is run from
/etc/inetd.conf, and is disabled by default on Red Hat systems.

%description -l pl
Tftp (trivial file transfer protocol) jest u¿ywany g³ównie do startowania
stacji bezdyskowych z sieci. Demon powinien byæ uruchamiany tylko wtedy, 
kiedy zachodzi taka konieczno¶æ. Tftpd jest uruchamiany przez inetd.

%prep
%setup -q -n netkit-%{name}-%{version}
%patch -p1 
%patch1 -p1 

%build
make

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT/{%{_bindir},/etc/sysconfig/rc-inetd,%{_sbindir},%{_mandir}/man{1,8}}

make install INSTALLROOT=$RPM_BUILD_ROOT \
	MANDIR=%{_mandir}

install %{SOURCE1} $RPM_BUILD_ROOT/etc/sysconfig/rc-inetd/tftpd

mv -f $RPM_BUILD_ROOT%{_sbindir}/in.tftpd $RPM_BUILD_ROOT/usr/sbin/tftpd
mv -f $RPM_BUILD_ROOT%{_mandir}/man8/in.tftpd.8 $RPM_BUILD_ROOT%{_mandir}/man8/tftpd.8

gzip -9nf README $RPM_BUILD_ROOT%{_mandir}/man*/*

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc README.gz
%attr(755,root,root) %{_bindir}/*
%attr(700,root,root) %{_sbindir}/*
%attr(640,root,root) /etc/sysconfig/rc-inetd/tftpd
%{_mandir}/man[18]/*
