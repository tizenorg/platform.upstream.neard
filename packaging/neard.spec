Name:       neard
Summary:    Near Field Communication Manager
Version:    0.12
Release:    1
Group:      Connectivity/NFC
License:    GPL-2.0
URL:        http://git.kernel.org/pub/scm/network/nfc/neard.git
Source0:    http://www.kernel.org/pub/linux/network/nfc/neard-%{version}.tar.bz2
Source1:    neard.service
Source1001: neard.manifest
BuildRequires:  pkgconfig(glib-2.0)
BuildRequires:  pkgconfig(dbus-1)
BuildRequires:  pkgconfig(libnl-3.0)

Requires:   libnl3
Requires(post):   systemd
Requires(preun):  systemd
Requires(postun): systemd

%description
Near Field Communication Manager



%package devel
Summary:    Development files for NFC Manager
Requires:   %{name} = %{version}-%{release}

%description devel
neard-devel contains development files for use with neard.

%package test
Summary:    Test Scripts for NFC Manager
Requires:   %{name} = %{version}-%{release}
Requires:   dbus-python
Requires:   pygobject

%description test
Scripts for testing neard and its functionality

%prep
%setup -q
cp %{SOURCE1001} .

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

# Systemd service file
install -d %{buildroot}%{_unitdir}
install -m 644 %{S:1} %{buildroot}%{_unitdir}/neard.service
install -d %{buildroot}%{_unitdir}/network.target.wants/
ln -s ../neard.service %{buildroot}%{_unitdir}/network.target.wants/neard.service


mkdir -p %{buildroot}%{_sysconfdir}/neard
cp src/main.conf %{buildroot}%{_sysconfdir}/neard/main.conf

%post
systemctl daemon-reload
systemctl restart neard.service

%preun
systemctl stop neard.service

%postun
systemctl daemon-reload

%files
%manifest %{name}.manifest
%license COPYING
%{_mandir}/man*/*
%{_libexecdir}/nfc/neard
%config %{_sysconfdir}/neard/main.conf
%config %{_sysconfdir}/dbus-1/system.d/org.neard.conf
%{_unitdir}/neard.service
%{_unitdir}/network.target.wants/neard.service

%files devel
%manifest %{name}.manifest
%{_includedir}/near/*.h
%{_libdir}/pkgconfig/*.pc

%files test
%manifest %{name}.manifest
%defattr(-,root,root,-)
%{_libdir}/neard/test/*
