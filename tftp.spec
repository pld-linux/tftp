Summary:	Client for the Trivial File Transfer Protocol (TFTP)
Summary(de):	Client für das 'trivial file transfer protocol (tftp)'
Summary(fr):	Client pour le « trivial file transfer protocol » (tftp)
Summary(pl):	Klient TFTP (Trivial File Transfer Protocol)
Summary(tr):	Ýlkel dosya aktarým protokolu (TFTP) için sunucu ve istemci
Name:		tftp
Version:	0.17
Release:	19
License:	BSD
Group:		Applications/Networking
Source0:	ftp://ftp.linux.org.uk/pub/linux/Networking/netkit/netkit-%{name}-%{version}.tar.gz
Source1:	%{name}d.inetd
Patch0:		%{name}-configure.patch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)
Obsoletes:	tftp-hpa

%description
The Trivial File Transfer Protocol (TFTP) is normally used only for
booting diskless workstations. This package contains tftp client.

%description -l de
Das trivial file transfer protocol (tftp) wird in der Regel nur zum
Booten von disklosen Workstations benutzt. Es bietet nur geringe
Sicherheit und sollte nur im Bedarfsfall aktiviert werden.

%description -l fr
Le « trivial file transfer protocol » (tftp) est normalement utilisé
uniquement pour démarrer les stations de travail sans disque. Il offre
très peu de sécurité et ne devrait pas être activé sauf si c'est
nécessaire.

%description -l pl
Tftp (trivial file transfer protocol) jest u¿ywany g³ównie do
startowania stacji bezdyskowych z sieci. Pakiet ten zawiera aplikacjê
tftp klienta.

%description -l tr
Ýlkel dosya aktarým protokolu genelde disksiz iþ istasyonlarýnýn að
üzerinden açýlmalarýnda kullanýlýr. Güvenlik denetimleri çok az
olduðundan zorunlu kalmadýkça çalýþtýrýlmamalýdýr.

%package -n tftpd
Summary:	Daemon for the trivial file transfer protocol (tftp)
Summary(de):	Dämon für das 'trivial file transfer protocol (tftp)'
Summary(fr):	Démon pour le « trivial file transfer protocol » (tftp)
Summary(pl):	Serwer tftp (trivial file transfer protocol)
Summary(tr):	Ýlkel dosya aktarým protokolu (TFTP) için sunucu ve istemci
Group:		Networking/Daemons
PreReq:		rc-inetd >= 0.8.1
Requires(pre):	/bin/id
Requires(pre):	/usr/sbin/useradd
Requires(postun):	/usr/sbin/userdel
Requires:	inetdaemon
Provides:	tftpdaemon
Obsoletes:	tftp-server
Obsoletes:	utftpd

%description -n tftpd
The Trivial File Transfer Protocol (TFTP) is normally used only for
booting diskless workstations. The tftp package provides the user
interface for TFTP, which allows users to transfer files to and from a
remote machine. It provides very little security, and should not be
enabled unless it is needed.

%description -n tftpd -l de
Das trivial file transfer protocol (tftp) wird in der Regel nur zum
Booten von disklosen Workstations benutzt. Es bietet nur geringe
Sicherheit und sollte nur im Bedarfsfall aktiviert werden.

%description -n tftpd -l fr
Le « trivial file transfer protocol » (tftp) est normalement utilisé
uniquement pour démarrer les stations de travail sans disque. Il offre
très peu de sécurité et ne devrait pas être activé sauf si c'est
nécessaire.

%description -n tftpd -l pl
TFTP (Trivial File Transfer Protocol) jest u¿ywany g³ównie do
startowania stacji bezdyskowych z sieci. Serwer tftp powinien byæ
instalowany tylko wtedy, kiedy zachodzi taka konieczno¶æ poniewa¿
nale¿y on do aplikacji o niskim poziomie bezpieczeñstwa.

%prep
%setup -q -n netkit-%{name}-%{version}
%patch0 -p1

%build
CFLAGS="%{rpmcflags}"; export CFLAGS

./configure \
	--with-c-compiler=gcc
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT/{%{_bindir},%{_sbindir},/etc/sysconfig/rc-inetd} \
	$RPM_BUILD_ROOT{%{_mandir}/man{1,8},/var/lib/tftp}

%{__make} install \
	INSTALLROOT=$RPM_BUILD_ROOT \
	MANDIR=%{_mandir}

install %{SOURCE1} $RPM_BUILD_ROOT/etc/sysconfig/rc-inetd/tftpd

mv -f $RPM_BUILD_ROOT%{_sbindir}/in.tftpd $RPM_BUILD_ROOT%{_sbindir}/tftpd
mv -f $RPM_BUILD_ROOT%{_mandir}/man8/in.tftpd.8 $RPM_BUILD_ROOT%{_mandir}/man8/tftpd.8

%clean
rm -rf $RPM_BUILD_ROOT

%pre -n tftpd
if [ -n "`id -u tftp 2>/dev/null`" ]; then
	if [ "`id -u tftp`" != "15" ]; then
		echo "Error: user tftp doesn't have uid=15. Correct this before installing tftpd." 1>&2
		exit 1
	fi
else
	echo "Adding user tftp UID=15."
	/usr/sbin/useradd -u 15 -r -d /var/lib/tftp -s /bin/false -c "TFTP User" -g ftp tftp 1>&2
fi

%post -n tftpd
if [ -f /var/lock/subsys/rc-inetd ]; then
	/etc/rc.d/init.d/rc-inetd reload 1>&2
else
	echo "Type \"/etc/rc.d/init.d/rc-inetd start\" to start inet server." 1>&2
fi

%postun -n tftpd
if [ "$1" = "0" -a -f /var/lock/subsys/rc-inetd ]; then
	/etc/rc.d/init.d/rc-inetd reload
fi
if [ "$1" = "0" ]; then
        echo "Removing user tftp."
	/usr/sbin/userdel tftp
fi

%files
%defattr(644,root,root,755)
%doc README
%attr(755,root,root) %{_bindir}/*
%{_mandir}/man1/*

%files -n tftpd
%defattr(644,root,root,755)
%attr(755,root,root) %{_sbindir}/*
%attr(640,root,root) %config %verify(not size mtime md5) /etc/sysconfig/rc-inetd/tftpd
%attr(750,tftp,root) %dir /var/lib/tftp
%{_mandir}/man8/*
