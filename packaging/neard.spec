Name:       neard-tizen
Summary:    Near Field Communication Manager
Version:    0.8
Release:    1
Group:      System/Networking
License:    GPLv2
Source0:    http://www.kernel.org/pub/linux/network/nfc/neard-%{version}.tar.bz2
Source1:    init
Source2:    neard.service
Requires(post): /bin/ln
BuildRequires:  pkgconfig(glib-2.0)
BuildRequires:  pkgconfig(dbus-1)
BuildRequires:  pkgconfig(libnl-2.0)

Requires:   systemd
Requires(post):   systemd
Requires(preun):  systemd
Requires(postun): systemd

%description
Near Field Communication Manager



%package devel
Summary:    Development files for NFC Manager
Group:      Development/Libraries
Requires:   %{name} = %{version}-%{release}

%description devel
neard-devel contains development files for use with neard.

%package test
Summary:    Test Scripts for NFC Manager
Group:      Development/Tools
Requires:   %{name} = %{version}-%{release}
Requires:   dbus-python
Requires:   pygobject

%description test
Scripts for testing neard and its functionality

%prep
%setup -q

%build
./bootstrap
%configure \
		--enable-debug \
		--prefix=/usr \
		--sysconfdir=/etc \
		--enable-nfctype1=builtin \
		--enable-nfctype2=builtin \
		--enable-nfctype3=builtin \
		--enable-nfctype4=builtin \
		--enable-p2p=builtin \
		--enable-test

make %{?jobs:-j%jobs}

%install
%make_install

mkdir -p %{buildroot}/etc/rc.d/init.d
cp %{SOURCE1} %{buildroot}/etc/rc.d/init.d/neard
chmod +x %{buildroot}/etc/rc.d/init.d/neard

# Systemd service file
install -d %{buildroot}%{_libdir}/systemd/system/
install -m 644 %{S:2} %{buildroot}%{_libdir}/systemd/system/neard.service
install -d %{buildroot}%{_libdir}/systemd/system/network.target.wants/
ln -s ../neard.service %{buildroot}%{_libdir}/systemd/system/network.target.wants/neard.service

%post
ln -sf ../init.d/neard /etc/rc.d/rc3.d/S64neard
systemctl daemon-reload
systemctl restart neard.service

%preun
systemctl stop neard.service

%postun
systemctl daemon-reload

%files
%doc COPYING
/usr/libexec/neard
/etc/dbus-1/system.d/org.neard.conf
/etc/rc.d/init.d/*
%{_libdir}/systemd/system/neard.service
%{_libdir}/systemd/system/network.target.wants/neard.service

%files devel
%{_includedir}/near/*.h
%{_libdir}/pkgconfig/*.pc

%files test
%defattr(-,root,root,-)
%{_libdir}/neard/test/*
