Summary:     Client and daemon for the trivial file transfer protocol (tftp)
Summary(pl): Klient i demon tftp (trivial file transfer protocol)
Name:        tftp
Version:     0.10
Release:     5
Copyright:   BSD
Group:       Networking
Source:      ftp://sunsite.unc.edu/pub/Linux/system/network/file-transfer/netkit-%{name}-%{version}.tar.gz
Patch:       %{name}-%{version}-misc.patch
Patch1:      %{name}-%{version}-security.patch
Requires:    inetd
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
install -d $RPM_BUILD_ROOT/usr/{bin,sbin,man/man1,man/man8}

make INSTALLROOT=$RPM_BUILD_ROOT install

mv -f $RPM_BUILD_ROOT%{_sbindir}/in.tftpd $RPM_BUILD_ROOT/usr/sbin/tftpd
mv -f $RPM_BUILD_ROOT%{_mandir}/man8/in.tftpd.8 $RPM_BUILD_ROOT/usr/man/man8/tftpd.8

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc README
%attr(755,root,root) %{_bindir}/*
%attr(700,root,root) %{_sbindir}/*
%{_mandir}/man[18]/*
