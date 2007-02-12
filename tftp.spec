Summary:	Client for the Trivial File Transfer Protocol (TFTP)
Summary(de.UTF-8):	Client für das 'trivial file transfer protocol (tftp)'
Summary(fr.UTF-8):	Client pour le « trivial file transfer protocol » (tftp)
Summary(pl.UTF-8):	Klient TFTP (Trivial File Transfer Protocol)
Summary(tr.UTF-8):	İlkel dosya aktarım protokolu (TFTP) için sunucu ve istemci
Name:		tftp
Version:	0.17
Release:	28
License:	BSD
Group:		Applications/Networking
Source0:	ftp://ftp.linux.org.uk/pub/linux/Networking/netkit/netkit-%{name}-%{version}.tar.gz
# Source0-md5:	b7262c798e2ff50e29c2ff50dfd8d6a8
Source1:	%{name}d.inetd
Patch0:		%{name}-configure.patch
BuildRequires:	rpmbuild(macros) >= 1.268
Obsoletes:	inetutils-tftp
Obsoletes:	tftp-hpa
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
The Trivial File Transfer Protocol (TFTP) is normally used only for
booting diskless workstations. This package contains tftp client.

%description -l de.UTF-8
Das trivial file transfer protocol (tftp) wird in der Regel nur zum
Booten von disklosen Workstations benutzt. Es bietet nur geringe
Sicherheit und sollte nur im Bedarfsfall aktiviert werden.

%description -l fr.UTF-8
Le « trivial file transfer protocol » (tftp) est normalement utilisé
uniquement pour démarrer les stations de travail sans disque. Il offre
très peu de sécurité et ne devrait pas être activé sauf si c'est
nécessaire.

%description -l pl.UTF-8
Tftp (trivial file transfer protocol) jest używany głównie do
startowania stacji bezdyskowych z sieci. Pakiet ten zawiera aplikację
tftp klienta.

%description -l tr.UTF-8
İlkel dosya aktarım protokolu genelde disksiz iş istasyonlarının ağ
üzerinden açılmalarında kullanılır. Güvenlik denetimleri çok az
olduğundan zorunlu kalmadıkça çalıştırılmamalıdır.

%package -n tftpd
Summary:	Daemon for the trivial file transfer protocol (tftp)
Summary(de.UTF-8):	Dämon für das 'trivial file transfer protocol (tftp)'
Summary(fr.UTF-8):	Démon pour le « trivial file transfer protocol » (tftp)
Summary(pl.UTF-8):	Serwer tftp (trivial file transfer protocol)
Summary(tr.UTF-8):	İlkel dosya aktarım protokolu (TFTP) için sunucu ve istemci
Group:		Networking/Daemons
Requires(postun):	/usr/sbin/userdel
Requires(pre):	/bin/id
Requires(pre):	/usr/sbin/useradd
Requires:	rc-inetd >= 0.8.1
Provides:	tftpdaemon
Provides:	user(tftp)
Obsoletes:	atftpd
Obsoletes:	inetutils-tftpd
Obsoletes:	tftp-server
Obsoletes:	tftpd-hpa
Obsoletes:	utftpd

%description -n tftpd
The Trivial File Transfer Protocol (TFTP) is normally used only for
booting diskless workstations. The tftp package provides the user
interface for TFTP, which allows users to transfer files to and from a
remote machine. It provides very little security, and should not be
enabled unless it is needed.

%description -n tftpd -l de.UTF-8
Das trivial file transfer protocol (tftp) wird in der Regel nur zum
Booten von disklosen Workstations benutzt. Es bietet nur geringe
Sicherheit und sollte nur im Bedarfsfall aktiviert werden.

%description -n tftpd -l fr.UTF-8
Le « trivial file transfer protocol » (tftp) est normalement utilisé
uniquement pour démarrer les stations de travail sans disque. Il offre
très peu de sécurité et ne devrait pas être activé sauf si c'est
nécessaire.

%description -n tftpd -l pl.UTF-8
TFTP (Trivial File Transfer Protocol) jest używany głównie do
startowania stacji bezdyskowych z sieci. Serwer tftp powinien być
instalowany tylko wtedy, kiedy zachodzi taka konieczność ponieważ
należy on do aplikacji o niskim poziomie bezpieczeństwa.

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
install -d $RPM_BUILD_ROOT{%{_bindir},%{_sbindir},/etc/sysconfig/rc-inetd} \
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
%useradd -P tftpd -u 15 -r -d /var/lib/tftp -s /bin/false -c "TFTP User" -g ftp tftp

%post -n tftpd
%service -q rc-inetd reload

%postun -n tftpd
if [ "$1" = "0" ]; then
	%service -q rc-inetd reload
	%userremove tftp
fi

%files
%defattr(644,root,root,755)
%doc README
%attr(755,root,root) %{_bindir}/*
%{_mandir}/man1/*

%files -n tftpd
%defattr(644,root,root,755)
%attr(755,root,root) %{_sbindir}/*
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) /etc/sysconfig/rc-inetd/tftpd
%attr(750,tftp,root) %dir /var/lib/tftp
%{_mandir}/man8/*
