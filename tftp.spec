Summary:	Client for the trivial file transfer protocol (tftp)
Summary(pl):	Klient tftp (trivial file transfer protocol)
Name:		tftp
Version:	0.10
Release:	5
Copyright:	BSD
Group:		Networking
Source:		ftp://sunsite.unc.edu/pub/Linux/system/network/file-transfer/netkit-%{name}-%{version}.tar.gz
Source1:	tftpd.inetd
Patch:		%{name}-%{version}-misc.patch
Patch1:		%{name}-%{version}-security.patch
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

%package -n tftpd
Summary:	Daemon for the trivial file transfer protocol (tftp)
Summary(pl):	Serwer tftp (trivial file transfer protocol)
Group:		Networking/Daemons
Requires:	inetdaemon
Requires:	rc-inetd

%description -n tftpd
The trivial file transfer protocol (tftp) is normally used only for 
booting diskless workstations. It provides very little security, and
should not be enabled unless it is needed. The tftp server is run from
inetd.

%description -n tftpd -l pl
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

%post -n tftpd
if [ -f /var/lock/subsys/rc-inetd ]; then
	/etc/rc.d/init.d/rc-inetd restart 1>&2
else
	echo "Type \"/etc/rc.d/init.d/rc-inetd start\" to start inet sever" 1>&2
fi

%postun -n tftpd
if [ -f /var/lock/subsys/rc-inetd ]; then
	/etc/rc.d/init.d/rc-inetd restart
fi

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc README.gz
%attr(755,root,root) %{_bindir}/*
%{_mandir}/man1/*

%files -n tftpd
%attr(755,root,root) %{_sbindir}/*
%attr(640,root,root) /etc/sysconfig/rc-inetd/tftpd
%{_mandir}/man8/*
