Summary:	Client for the Trivial File Transfer Protocol (TFTP)
Summary(pl):	Klient TFTP (Trivial File Transfer Protocol)
Name:		tftp
Version:	0.16
Release:	2
Copyright:	BSD
Group:		Networking/Daemons
Group(pl):	Sieciowe/Serwery
Source:		ftp://sunsite.unc.edu/pub/Linux/system/network/file-transfer/netkit-%{name}-%{version}.tar.gz
Source1:	tftpd.inetd
Patch:		tftp-configure.patch
BuildRoot:	/tmp/%{name}-%{version}-root

%description
The Trivial File Transfer Protocol (TFTP) is normally used only for 
booting diskless workstations. This package contains tftp client.

%description -l pl
Tftp (trivial file transfer protocol) jest u¿ywany g³ównie do startowania
stacji bezdyskowych z sieci. Pakiet ten zawira aplikacjê tftp klienta.

%package -n tftpd
Summary:	Daemon for the trivial file transfer protocol (tftp)
Summary(pl):	Serwer tftp (trivial file transfer protocol)
Group:		Networking/Daemons
Requires:	inetdaemon
Prereq:		rc-inetd >= 0.8.1

%description -n tftpd
The Trivial File Transfer Protocol (TFTP) is normally used only for booting
diskless workstations. The tftp package provides the user interface for
TFTP, which allows users to transfer files to and from a remote machine. It
provides very little security, and should not be enabled unless it is
needed.

%description -n tftpd -l pl
TFTP (Trivial File Transfer Protocol) jest u¿ywany g³ównie do startowania
stacji bezdyskowych z sieci. Serwer tftp powinien byæ instalowany tylko
wtedy, kiedy zachodzi taka konieczno¶æ poniewa¿ nale¿y on do aplikacji o
niskim poziomie bezpieczeñstwa.

%prep
%setup -q -n netkit-%{name}-%{version}
%patch -p1 
#%patch1 -p1 

%build
CFLAGS="$RPM_OPT_FLAGS" sh configure
make

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT/{%{_bindir},/etc/sysconfig/rc-inetd,%{_sbindir},%{_mandir}/man{1,8},var/state/tftp}

make install \
	INSTALLROOT=$RPM_BUILD_ROOT \
	MANDIR=%{_mandir}

install %{SOURCE1} $RPM_BUILD_ROOT/etc/sysconfig/rc-inetd/tftpd

mv -f $RPM_BUILD_ROOT%{_sbindir}/in.tftpd $RPM_BUILD_ROOT/usr/sbin/tftpd
mv -f $RPM_BUILD_ROOT%{_mandir}/man8/in.tftpd.8 $RPM_BUILD_ROOT%{_mandir}/man8/tftpd.8

gzip -9nf README $RPM_BUILD_ROOT%{_mandir}/man*/*

%post -n tftpd
if [ -f /var/lock/subsys/rc-inetd ]; then
	/etc/rc.d/init.d/rc-inetd reload 1>&2
else
	echo "Type \"/etc/rc.d/init.d/rc-inetd start\" to start inet sever" 1>&2
fi

%postun -n tftpd
if [ "$1" = "0" -a -f /var/lock/subsys/rc-inetd ]; then
	/etc/rc.d/init.d/rc-inetd reload
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
%attr(750,nobody,nobody) %dir /var/state/tftp
%{_mandir}/man8/*
