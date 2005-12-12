#
# Conditional build:
%bcond_without	dist_kernel	# without distribution kernel
%bcond_without	kernel		# don't build kernel modules
%bcond_without	userspace	# don't build userspace tools
%define		snap		20040919
#
Summary:	DXR3 and H+ driver
Summary(pl):	Sterowniki dla DXR3 i H+
Name:		em8300
Version:	0.14.0
Release:	3.%{snap}.1
License:	GPL
Group:		Applications/System
#Source0:	http://dl.sourceforge.net/dxr3/%{name}-%{version}.tar.gz
Source0:	http://www.kernel.pl/~adasi/%{name}-%{snap}.tar.bz2
# Source0-md5:	832f5a03826701a71193ca235973dd12
Source1:	%{name}.init
Source2:	%{name}.sysconf
Patch0:		%{name}-automake.patch
URL:		http://dxr3.sourceforge.net/
%if %{with userspace}
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	gtk+-devel >= 1.2.0
BuildRequires:	libtool
%endif
%if %{with kernel} && %{with dist_kernel}
BuildRequires:	kernel-headers 
BuildRequires:	rpmbuild(macros) >= 1.118
%endif
Requires(post,preun):	/sbin/chkconfig
Requires:	%{name}-libs = %{version}-%{release}
Provides:	dxr3
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
em8300 is a Linux driver for Creative DXR3 and Sigma Designs
Hollywood+ cards. Both cards are hardware MPEG1, MPEG2, AC3 decoders.
Additionaly Xine and MPlayer with help of this driver allow you to
play all the video formats that they recognise through the tv-out of
these cards.

%description -l pl
em8300 pozwala na uruchomienie pod Linuksem kart Creative DXR3 i Sigma
Designs Hollywood+. Obie karty, o prawie identycznej konstrukcji s±
sprzêtowymi dekoderami MPEG1, MPEG2 i AC3. Programy Xine i MPlayer
pozwalaj± przy u¿yciu tego sterownika na odtwarzanie przez wyj¶cie
telewizyjne tych kart nie tylko w/w formatów, ale tak¿e wszystkich
formatów video, które te programy rozpoznaj±.

%package libs
Summary:	libdxr3 library for DXR3/Hollywood+ cards
Summary(pl):	Biblioteka libdxr3 do kart DXR3/Hollywood+
Group:		Libraries

%description libs
libdxr3 library for DXR3/Hollywood+ cards.

%description libs -l pl
Biblioteka libdxr3 do kart DXR3/Hollywood+.

%package devel
Summary:	Files required to develop programs using em8300
Summary(pl):	Pliki potrzebne do tworzenia programów korzystaj±cych z em8300
Group:		Development/Libraries
Requires:	%{name}-libs = %{version}-%{release}

%description devel
Header files and additional scripts useful for developers of em8300
apps.

%description devel -l pl
Pliki nag³ówkowe i skrypty przydatne dla autorów aplikacji
korzystaj±cych z em8300.

%package static
Summary:	Static libraries for em8300
Summary(pl):	Statyczne biblioteki dla em8300
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
Static libraries for em8300.

%description static -l pl
Statyczne biblioteki dla em8300.

%package gtk
Summary:	Utility programs for em8300 using GTK+
Summary(pl):	Programy u¿ytkowe em8300 u¿ywaj±ce bibliteki GTK+
Group:		X11/Applications
Requires:	%{name} = %{version}-%{release}

%description gtk
Utility programs for em8300 using GTK+ toolkit.

%description gtk -l pl
Programy u¿ytkowe em8300 u¿ywaj±ce biblioteki GTK+.

%package -n kernel-video-em8300
Summary:	em8300 Linux kernel modules
Summary(pl):	Modu³y j±dra Linuksa em8300
Group:		Base/Kernel
%{?with_dist_kernel:%requires_releq_kernel_up}
Requires(post,postun):	/sbin/depmod

%description -n kernel-video-em8300
em8300 Linux kernel modules.

%description -n kernel-video-em8300 -l pl
Modu³y j±dra Linuksa em8300.

%package -n kernel-smp-video-em8300
Summary:	em8300 Linux SMP kernel modules
Summary(pl):	Modu³y j±dra Linuksa SMP em8300
Group:		Base/Kernel
%{?with_dist_kernel:%requires_releq_kernel_smp}
Requires(post,postun):	/sbin/depmod

%description -n kernel-smp-video-em8300
em8300 Linux SMP kernel modules.

%description -n kernel-smp-video-em8300 -l pl
Modu³y j±dra Linuksa SMP em8300.

%prep
%setup -q -n %{name}
%patch0 -p1

%build
%if %{with userspace}
%{__libtoolize}
%{__aclocal} -I autotools
%{__autoconf}
%{__autoheader}
%{__automake}
%configure
%{__make}
%endif

%if %{with kernel}
cd modules
rm -rf include
install -d include/{linux,config}
ln -sf %{_kernelsrcdir}/config-smp .config
ln -sf %{_kernelsrcdir}/include/linux/autoconf-up.h include/linux/autoconf.h
ln -sf %{_kernelsrcdir}/include/asm-%{_target_base_arch} include/asm
touch include/config/MARKER

%{__make} -C %{_kernelsrcdir} \
	KERNEL_LOCATION="%{_kernelsrcdir}" M=$PWD O=$PWD \
	EM8300_DEBUG="%{rpmcflags} -D__KERNEL_SMP" modules

for f in em8300.ko adv717x.ko bt865.ko; do
	mv -f $f $f.smp
done

%{__make} clean

%{__make} \
	KERNEL_LOCATION="%{_kernelsrcdir}" \
	EM8300_DEBUG="%{rpmcflags}"
%endif

%install
rm -rf $RPM_BUILD_ROOT

%if %{with userspace}
%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

mv -f modules/{INSTALL,INSTALL.modules}

install -D modules/em8300.uc $RPM_BUILD_ROOT%{_datadir}/misc/em8300.uc

install scripts/microcode_upload.pl $RPM_BUILD_ROOT%{_bindir}/em8300_microcode_upload

install -D %{SOURCE1} $RPM_BUILD_ROOT/etc/rc.d/init.d/%{name}
install -D %{SOURCE2} $RPM_BUILD_ROOT/etc/sysconfig/%{name}

rm -f $RPM_BUILD_ROOT%{_datadir}/em8300/{modules.tar.gz,em8300.sysv}
%endif

%if %{with kernel}
install -d $RPM_BUILD_ROOT/lib/modules/%{_kernel_ver}{,smp}/kernel/drivers/video
for f in em8300.ko adv717x.ko bt865.ko; do
	install modules/$f \
		$RPM_BUILD_ROOT/lib/modules/%{_kernel_ver}/kernel/drivers/video/$f
	install modules/$f.smp \
		$RPM_BUILD_ROOT/lib/modules/%{_kernel_ver}smp/kernel/drivers/video/$f
done
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%post
/sbin/chkconfig --add %{name}
if [ -f /var/lock/subsys/%{name} ]; then
	/etc/rc.d/init.d/%{name} restart 1>&2
else
	echo "Run \"/etc/rc.d/init.d/%{name} start\" to load %{name} modules."
fi

%preun
if [ "$1" = "0" ]; then
	if [ -f /var/lock/subsys/%{name} ]; then
		/etc/rc.d/init.d/%{name} stop 1>&2
	fi
	/sbin/chkconfig --del %{name}
fi

%post	libs -p /sbin/ldconfig
%postun	libs -p /sbin/ldconfig

%post	-n kernel-video-em8300
%depmod %{_kernel_ver}

%postun	-n kernel-video-em8300
%depmod %{_kernel_ver}

%post	-n kernel-smp-video-em8300
%depmod %{_kernel_ver}smp

%postun	-n kernel-smp-video-em8300
%depmod %{_kernel_ver}smp

%if %{with userspace}
%files
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog README modules/{README*,INSTALL*,devices.sh,devfs_symlinks}
%attr(755,root,root) %{_bindir}/em8300_microcode_upload
%{_datadir}/misc/em8300.uc
%dir %{_datadir}/em8300
%{_datadir}/em8300/em8300.pm
%attr(755,root,root) %{_datadir}/em8300/*.pl
%attr(754,root,root) /etc/rc.d/init.d/%{name}
%config(noreplace) %verify(not md5 mtime size) /etc/sysconfig/%{name}

%files libs
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/lib*.so.*.*.*

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/lib*.so
%{_libdir}/lib*.la
%{_includedir}/libdxr3
%{_includedir}/linux/em8300.h

%files static
%defattr(644,root,root,755)
%{_libdir}/lib*.a

%files gtk
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/autocal
%attr(755,root,root) %{_bindir}/dhc
%attr(755,root,root) %{_bindir}/dxr3view
%attr(755,root,root) %{_bindir}/em8300setup
%endif

%if %{with kernel}
%files -n kernel-video-em8300
%defattr(644,root,root,755)
/lib/modules/%{_kernel_ver}/kernel/drivers/video/*.ko*

%files -n kernel-smp-video-em8300
%defattr(644,root,root,755)
/lib/modules/%{_kernel_ver}smp/kernel/drivers/video/*.ko*
%endif
