Summary: BusyBox is a tiny suite of Unix utilities in a multi-call binary.
Name: busybox
Version: 1.22.1
Release: b1
License: GPL
Group: System Environment/Shells
Source: http://www.busybox.net/downloads/%{name}-%{version}.tar.bz2
URL: http://www.busybox.net
BuildRoot: %{_tmppath}/%{name}-root
#BuildRequires: libselinux-devel >= 1.27.7-2
#BuildRequires: libsepol-devel
BuildRequires: uClibc-devel
#BuildArchitectures: i586

Requires: filesystem

#Provides: cpio e2fsprogs = 1.38 gawk gzip hdparm iputils less mktemp
Provides: cpio gawk gzip hdparm iputils less mktemp hostname
Provides: passwd procps = 3.2.6 psmisc rdate sed telnet vi which
Provides: vim-common, vim-minimal, wget
#Provides: dhclient

%description
Busybox is a single binary which includes versions of a large number
of system commands, including a shell.  This package can be very
useful for recovering from certain types of system failures,
particularly those involving broken shared libraries.
normal use.

%prep
%setup -q
cp berry/defconfig .config
##SELINUX Patch
##%patch2 -b .selinux -p1
##%patch -b .static -p1
#%patch3 -b .cve-2006-1058 -p1

%build
yes "" | make oldconfig %{?_smp_mflags}
#CFLAGS=-I/usr/include LDFLAGS=-L/usr/lib
make CC="/usr/lib/uClibc/i386-uclibc-gcc" V=1 %{?_smp_mflags}
echo "pod2text in perl!!"

%install
rm -rf $RPM_BUILD_ROOT
#mkdir -p $RPM_BUILD_ROOT/sbin
#mkdir -p $RPM_BUILD_ROOT/%{_mandir}/man1
#install -m 755 busybox $RPM_BUILD_ROOT/sbin/busybox
#install -m 644 docs/BusyBox.1 $RPM_BUILD_ROOT/%{_mandir}/man1/busybox.1

sed -e "s:CONFIG_PREFIX=\"/var/tmp/busybox-root/\":CONFIG_PREFIX=\"$RPM_BUILD_ROOT\":" -i .config
make CC="/usr/lib/uClibc/i386-uclibc-gcc" PREFIX=$RPM_BUILD_ROOT install

mkdir -p $RPM_BUILD_ROOT/etc/
cat > $RPM_BUILD_ROOT/etc/busybox.conf<<EOM
[SUID]
ping       = ssx root.root
traceroute = ssx root.root
su         = ssx root.root
passwd     = ssx root.root
EOM
chmod +s $RPM_BUILD_ROOT/bin/busybox

# for link
#rm $RPM_BUILD_ROOT/usr/bin/{arping,basename,fuser,sort}
rm $RPM_BUILD_ROOT/usr/bin/{basename,fuser,sort}
for n in awk basename sort
do
	ln -s busybox $RPM_BUILD_ROOT/bin/$n
done
for n in arping fuser
do
	ln -s ../bin/busybox $RPM_BUILD_ROOT/sbin/$n
done
# Original cmd
#rm $RPM_BUILD_ROOT/bin/{chgrp,cp}
#rm $RPM_BUILD_ROOT/usr/bin/install
#cp -a berry/original/* $RPM_BUILD_ROOT

mkdir -p $RPM_BUILD_ROOT/usr/share/udhcpc/
#cp -a examples/udhcp/simple.script $RPM_BUILD_ROOT/usr/share/udhcpc/default.script
cp -a berry/udhcpc.script $RPM_BUILD_ROOT/usr/share/udhcpc/default.script
chmod +x $RPM_BUILD_ROOT/usr/share/udhcpc/default.script

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root)
/etc/busybox.conf
/bin/*
/sbin/*
/usr/*
#/sbin/busybox
#%{_mandir}/man1/busybox*
#%attr(4755,root,root) /bin/mount
#%attr(4755,root,root) /bin/umount

%changelog
* Mon Jan 20 2014 Yuichiro Nakada <berry@berry-lab.net>
- Update to 1.22.1
* Tue Jun 5 2012 Yuichiro Nakada <berry@rberry.co.cc>
- Update to 1.20.1
* Mon Mar 19 2012 Yuichiro Nakada <berry@rberry.co.cc>
- Update to 1.19.4
* Fri Aug 13 2010 Yuichiro Nakada <berry@rberry.co.cc>
- Update to 1.17.1
* Fri Jan 15 2010 Yuichiro Nakada <berry@rberry.co.cc>
- Update to 1.15.3
* Thu Oct 22 2009 Yuichiro Nakada <berry@po.yui.mine.nu>
- Update to 1.15.2
* Wed Jul 1 2009 Yuichiro Nakada <berry@po.yui.mine.nu>
- Update to 1.14.2
* Fri Nov 3 2006 Yuichiro Nakada <berry@po.yui.mine.nu>
- Update to 1.2.2.1
* Tue Oct 3 2006 Yuichiro Nakada <berry@po.yui.mine.nu>
- Create for Berry Linux
