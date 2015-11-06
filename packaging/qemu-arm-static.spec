#
# spec file for package qemu
#
# Copyright (c) 2013 SUSE LINUX Products GmbH, Nuernberg, Germany.
#
# All modifications and additions to the file contributed by third parties
# remain the property of their copyright owners, unless otherwise agreed
# upon. The license for this file, and modifications and additions to the
# file, is the same license as for the pristine package itself (unless the
# license for the pristine package is not an Open Source License, in which
# case the license is the MIT License). An "Open Source License" is a
# license that conforms to the Open Source Definition (Version 1.9)
# published by the Open Source Initiative.

# Please submit bugfixes or comments via http://bugs.opensuse.org/
#


Name:           qemu-arm-static
Url:            http://www.qemu.org/
Summary:        Universal CPU emulator
License:        BSD-3-Clause and GPL-2.0+ and LGPL-2.1+ and MIT
Group:          System/Emulators/PC
Version:        1.6.0rc3
Release:        0
Source:         qemu-1.6.0-rc3.tar.bz2
Source1:        qemu-binfmt-conf.sh
# this is to make lint happy
Source300:      rpmlintrc
BuildRoot:      %{_tmppath}/%{name}-%{version}-build

BuildRequires:  python
BuildRequires:  libattr-devel
%if 0%{?suse_version} >= 1220
BuildRequires:  pcre-devel-static
%endif
%if 0%{?suse_version}
BuildRequires:  glibc-devel-static
BuildRequires:  libattr-devel-static
BuildRequires:  glib2-devel-static
BuildRequires:  zlib-devel-static
%else
BuildRequires:  glibc-static
BuildRequires:  glib2-static
BuildRequires:  zlib-static
%endif

Provides:       qemu:%_bindir/qemu-arm-static
Provides:       tizen-qemu-arm-static = 2013.12.12

%description
QEMU is an extremely well-performing CPU emulator that allows you to
choose between simulating an entire system and running userspace
binaries for different architectures under your native operating
system. It currently emulates x86, ARM, PowerPC and SPARC CPUs as well
as PC and PowerMac systems.

%prep
%setup -q -n qemu-1.6.0-rc3

%build

export LDFLAGS="-lrt -pthread -lgthread-2.0 -lglib-2.0"
./configure \
	--prefix=%_prefix \
	--sysconfdir=%_sysconfdir \
	--libexecdir=%_libexecdir \
	--target-list="arm-linux-user,arm64-linux-user" \
	--disable-tools \
	--disable-guest-agent \
	--disable-docs \
	--disable-system \
	--enable-linux-user \
	--disable-werror \
	--disable-linux-aio \
	--disable-fdt \
	--disable-sdl \
	--static

%if 0%{?suse_version} >= 1230 || 0%{?fedora} >= 19 || 0%{?centos_version} == 700
# -lrt needs to come after -lglib-2.0 to avoid undefined mq_open, mq_xxx
sed -i "s/-lglib-2.0/-lglib-2.0 -lrt/" config-host.mak
%endif

make %{?jobs:-j%jobs} V=1

%install
make install DESTDIR=$RPM_BUILD_ROOT
install -d -m 755 $RPM_BUILD_ROOT/%_sbindir
install -m 755 %{SOURCE1} $RPM_BUILD_ROOT/%_sbindir
mv $RPM_BUILD_ROOT/%_bindir/qemu-arm $RPM_BUILD_ROOT/%_bindir/qemu-arm-static
mv $RPM_BUILD_ROOT/%_bindir/qemu-arm64 $RPM_BUILD_ROOT/%_bindir/qemu-arm64-static
rm -rf $RPM_BUILD_ROOT/%_datadir
rm -rf $RPM_BUILD_ROOT/%_sysconfdir
rm -rf $RPM_BUILD_ROOT/%_libexecdir
#%fdupes -s $RPM_BUILD_ROOT

%clean
rm -rf ${RPM_BUILD_ROOT}

%files
%defattr(-, root, root)
%{_bindir}/qemu-arm-static
%{_bindir}/qemu-arm64-static
%{_sbindir}/*

%changelog
