%define kernel_version 3.0
%define kernel_target adaptation-bb
Name:       neard
Summary:    Near Field Communication Manager
Version:    0.2.26.g7bf4d39
Release:    1
Group:      System/Networking
License:    TOBE/FILLED
Source0:    http://www.kernel.org/pub/linux/network/nfc/neard-%{version}.tar.bz2
Source1:    init
Requires(post): /bin/ln
BuildRequires:  pkgconfig(glib-2.0)
BuildRequires:  pkgconfig(dbus-1)
BuildRequires:  pkgconfig(libnl-1)
BuildRequires:  kernel-adaptation-bb-devel

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
Requires:   pygobject2  
  
%description test  
Scripts for testing neard and its functionality  

%prep
%setup -q

%build
kver=`find /lib/modules -name "%{kernel_version}*%{kernel_target}" | cut -c 14-`
CFLAGS+=" -I/usr/src/kernels/${kver}/include"
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

%post
ln -sf ../init.d/neard /etc/rc.d/rc3.d/S64neard

%files
%doc COPYING
/usr/libexec/neard
/etc/rc.d/init.d/*

%files devel
%{_includedir}/near/*.h
%{_libdir}/pkgconfig/*.pc

%files test  
%defattr(-,root,root,-)  
%{_libdir}/%{name}/test/* 
