Summary:	Client for the Trivial File Transfer Protocol (TFTP)
Summary(de):	Client f�r das 'trivial file transfer protocol (tftp)'
Summary(fr):	Client pour le � trivial file transfer protocol � (tftp)
Summary(pl):	Klient TFTP (Trivial File Transfer Protocol)
Summary(tr):	�lkel dosya aktar�m protokolu (TFTP) i�in sunucu ve istemci
Name:		tftp
Version:	0.16
Release:	8
License:	BSD
Group:		Applications/Networking
Group(pl):	Aplikacje/Sieciowe
Source0:	ftp://sunsite.unc.edu/pub/Linux/system/network/file-transfer/netkit-%{name}-%{version}.tar.gz
Source1:	tftpd.inetd
Patch0:		tftp-configure.patch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
The Trivial File Transfer Protocol (TFTP) is normally used only for
booting diskless workstations. This package contains tftp client.

%description -l de
Das trivial file transfer protocol (tftp) wird in der Regel nur zum
Booten von disklosen Workstations benutzt. Es bietet nur geringe
Sicherheit und sollte nur im Bedarfsfall aktiviert werden.

%description -l fr
Le � trivial file transfer protocol � (tftp) est normalement utilis�
uniquement pour d�marrer les stations de travail sans disque. Il offre
tr�s peu de s�curit� et ne devrait pas �tre activ� sauf si c'est
n�cessaire.

%description -l pl
Tftp (trivial file transfer protocol) jest u�ywany g��wnie do
startowania stacji bezdyskowych z sieci. Pakiet ten zawira aplikacj�
tftp klienta.

%description -l tr
�lkel dosya aktar�m protokolu genelde disksiz i� istasyonlar�n�n a�
�zerinden a��lmalar�nda kullan�l�r. G�venlik denetimleri �ok az
oldu�undan zorunlu kalmad�k�a �al��t�r�lmamal�d�r.

%package -n tftpd
Summary:	Daemon for the trivial file transfer protocol (tftp)
Summary(de):	D�mon f�r das 'trivial file transfer protocol (tftp)'
Summary(fr):	D�mon pour le � trivial file transfer protocol � (tftp)
Summary(pl):	Serwer tftp (trivial file transfer protocol)
Summary(tr):	�lkel dosya aktar�m protokolu (TFTP) i�in sunucu ve istemci
Group:		Networking/Daemons
Requires:	inetdaemon
Prereq:		rc-inetd >= 0.8.1
Obsoletes:	tftp-server

%description -n tftpd
The Trivial File Transfer Protocol (TFTP) is normally used only for
booting diskless workstations. The tftp package provides the user
interface for TFTP, which allows users to transfer files to and from a
remote machine. It provides very little security, and should not be
enabled unless it is needed.

%description -l de -n tftpd
Das trivial file transfer protocol (tftp) wird in der Regel nur zum
Booten von disklosen Workstations benutzt. Es bietet nur geringe
Sicherheit und sollte nur im Bedarfsfall aktiviert werden.

%description -l fr -n tftpd
Le � trivial file transfer protocol � (tftp) est normalement utilis�
uniquement pour d�marrer les stations de travail sans disque. Il offre
tr�s peu de s�curit� et ne devrait pas �tre activ� sauf si c'est
n�cessaire.

%description -n tftpd -l pl
TFTP (Trivial File Transfer Protocol) jest u�ywany g��wnie do
startowania stacji bezdyskowych z sieci. Serwer tftp powinien by�
instalowany tylko wtedy, kiedy zachodzi taka konieczno�� poniewa�
nale�y on do aplikacji o niskim poziomie bezpiecze�stwa.

%prep
%setup -q -n netkit-%{name}-%{version}
%patch -p1 
#%patch1 -p1 

%build
CFLAGS="$RPM_OPT_FLAGS" sh configure
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT/{%{_bindir},/etc/sysconfig/rc-inetd,%{_sbindir},%{_mandir}/man{1,8},var/lib/tftp}

%{__make} install \
	INSTALLROOT=$RPM_BUILD_ROOT \
	MANDIR=%{_mandir}

install %{SOURCE1} $RPM_BUILD_ROOT/etc/sysconfig/rc-inetd/tftpd

mv -f $RPM_BUILD_ROOT%{_sbindir}/in.tftpd $RPM_BUILD_ROOT%{_sbindir}/tftpd
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
%defattr(644,root,root,755)
%attr(755,root,root) %{_sbindir}/*
%attr(640,root,root) %config %verify(not size mtime md5) 
%attr(640,root,root) /etc/sysconfig/rc-inetd/tftpd
%attr(750,nobody,nobody) %dir /var/lib/tftp
%{_mandir}/man8/*
