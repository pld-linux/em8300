# TODO
# - cc
#
# Conditional build:
%bcond_without	dist_kernel	# allow non-distribution kernel
%bcond_without	kernel		# don't build kernel modules
%bcond_without	up		# don't build UP module
%bcond_without	smp		# don't build SMP module
%bcond_without	userspace	# don't build userspace tools
%bcond_with	verbose		# verbose build (V=1)
%bcond_with	grsec_kernel	# build for kernel-grsecurity

%ifarch sparc
# kernel modules won't build on sparc32, no I2C in kernel
%undefine	with_kernel
%endif

%if %{without kernel}
%undefine	with_dist_kernel
%endif
%if %{with kernel} && %{with dist_kernel} && %{with grsec_kernel}
%define	alt_kernel	grsecurity
%endif
%if "%{_alt_kernel}" != "%{nil}"
%undefine	with_userspace
%endif

%define		_rel	59
%define		pname	em8300
Summary:	DXR3 and H+ driver
Summary(pl):	Sterowniki dla DXR3 i H+
Name:		%{pname}%{_alt_kernel}
Version:	0.16.0
Release:	%{_rel}
License:	GPL
Group:		Applications/System
Source0:	http://dl.sourceforge.net/dxr3/%{pname}-%{version}.tar.gz
# Source0-md5:	9e9b769b99927079b4fd6ec423d95049
Source1:	%{pname}.init
Source2:	%{pname}.sysconf
Patch0:		%{pname}-make.patch
URL:		http://dxr3.sourceforge.net/
%if %{with userspace}
BuildRequires:	autoconf >= 2.13
BuildRequires:	automake
BuildRequires:	gtk+2-devel >= 1:2.0.0
BuildRequires:	pkgconfig
%endif
%if %{with kernel}
%{?with_dist_kernel:BuildRequires:	kernel%{_alt_kernel}-module-build >= 3:2.6.14}
BuildRequires:	rpmbuild(macros) >= 1.308
%endif
Requires(post,preun):	/sbin/chkconfig
Requires:	rc-scripts
Provides:	dxr3
Obsoletes:	em8300-libs
%if %{without userspace}
ExcludeArch:	sparc
%endif
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

%package devel
Summary:	Header file to communicate with em8300 Linux kernel modules
Summary(pl):	Plik nag³ówkowy do komunikacji z modu³ami j±dra Linuksa em8300
Group:		Development/Libraries
Obsoletes:	em8300-static

%description devel
Header file to communicate with em8300 Linux kernel modules.

%description devel -l pl
Plik nag³ówkowy do komunikacji z modu³ami j±dra Linuksa em8300.

%package gtk
Summary:	Utility programs for em8300 using GTK+
Summary(pl):	Programy u¿ytkowe em8300 u¿ywaj±ce bibliteki GTK+
Group:		X11/Applications
Requires:	%{pname} = %{version}-%{release}

%description gtk
Utility programs for em8300 using GTK+ toolkit.

%description gtk -l pl
Programy u¿ytkowe em8300 u¿ywaj±ce biblioteki GTK+.

%package -n kernel%{_alt_kernel}-video-em8300
Summary:	em8300 Linux kernel modules
Summary(pl):	Modu³y j±dra Linuksa em8300
Group:		Base/Kernel
Release:	%{_rel}@%{_kernel_ver_str}
Requires(post,postun):	/sbin/depmod
%if %{with dist_kernel}
%requires_releq_kernel_up
Requires(postun):	%releq_kernel_up
%endif

%description -n kernel%{_alt_kernel}-video-em8300
em8300 Linux kernel modules.

%description -n kernel%{_alt_kernel}-video-em8300 -l pl
Modu³y j±dra Linuksa em8300.

%package -n kernel%{_alt_kernel}-smp-video-em8300
Summary:	em8300 Linux SMP kernel modules
Summary(pl):	Modu³y j±dra Linuksa SMP em8300
Release:	%{_rel}@%{_kernel_ver_str}
Group:		Base/Kernel
Requires(post,postun):	/sbin/depmod
%if %{with dist_kernel}
%requires_releq_kernel_smp
Requires(postun):	%releq_kernel_smp
%endif

%description -n kernel%{_alt_kernel}-smp-video-em8300
em8300 Linux SMP kernel modules.

%description -n kernel%{_alt_kernel}-smp-video-em8300 -l pl
Modu³y j±dra Linuksa SMP em8300.

%prep
%setup -q -n %{pname}-%{version}
%patch0 -p0

%build
%if %{with userspace}
%{__aclocal} -I autotools
%{__autoconf}
%{__autoheader}
%{__automake}
%configure
%{__make}
%endif

%if %{with kernel}
cd modules
for cfg in %{?with_dist_kernel:%{?with_smp:smp} up}%{!?with_dist_kernel:nondist}; do
	if [ ! -r "%{_kernelsrcdir}/config-$cfg" ]; then
		exit 1
	fi
	install -d o/include/linux
	ln -sf %{_kernelsrcdir}/config-$cfg o/.config
	ln -sf %{_kernelsrcdir}/Module.symvers-$cfg o/Module.symvers
	ln -sf %{_kernelsrcdir}/include/linux/autoconf-$cfg.h o/include/linux/autoconf.h
%if %{with dist_kernel}
	%{__make} -j1 -C %{_kernelsrcdir} O=$PWD/o prepare scripts
%endif
	install -d o/include/config
	touch o/include/config/MARKER
	ln -sf %{_kernelsrcdir}/scripts o/scripts

	cp ../include/linux/em8300.h o/include/linux/em8300.h

	%{__make} -C %{_kernelsrcdir} clean \
		RCS_FIND_IGNORE="-name '*.ko' -o" \
		SYSSRC=%{_kernelsrcdir} \
		SYSOUT=$PWD/o \
		M=$PWD O=$PWD/o \
		%{?with_verbose:V=1}
	%{__make} -C %{_kernelsrcdir} modules \
			CC="%{__cc}" CPP="%{__cpp}" \
		SYSSRC=%{_kernelsrcdir} \
		SYSOUT=$PWD/o \
		M=$PWD O=$PWD/o \
		%{?with_verbose:V=1}

	for i in em8300 adv717x bt865; do
		mv $i{,-$cfg}.ko
	done
done
%endif

%install
rm -rf $RPM_BUILD_ROOT

%if %{with userspace}
%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

install -D %{SOURCE1} $RPM_BUILD_ROOT/etc/rc.d/init.d/%{pname}
install -D %{SOURCE2} $RPM_BUILD_ROOT/etc/sysconfig/%{pname}
%endif

%if %{with kernel}
install -d $RPM_BUILD_ROOT/lib/modules/%{_kernel_ver}{,smp}/kernel/drivers/video
for i in adv717x bt865 em8300; do
	install modules/$i-%{?with_dist_kernel:up}%{!?with_dist_kernel:nondist}.ko \
		$RPM_BUILD_ROOT/lib/modules/%{_kernel_ver}/kernel/drivers/video/$i.ko
done
%if %{with smp} && %{with dist_kernel}
for i in adv717x bt865 em8300; do
	install modules/$i-smp.ko \
		$RPM_BUILD_ROOT/lib/modules/%{_kernel_ver}smp/kernel/drivers/video/$i.ko
done
%endif
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%post
/sbin/chkconfig --add %{pname}
%service %{pname} restart

%preun
if [ "$1" = "0" ]; then
	%service stop
	/sbin/chkconfig --del %{pname}
fi

%post	-n kernel%{_alt_kernel}-video-em8300
%depmod %{_kernel_ver}

%postun	-n kernel%{_alt_kernel}-video-em8300
%depmod %{_kernel_ver}

%post	-n kernel%{_alt_kernel}-smp-video-em8300
%depmod %{_kernel_ver}smp

%postun	-n kernel%{_alt_kernel}-smp-video-em8300
%depmod %{_kernel_ver}smp

%if %{with userspace}
%files
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog README modules/README*
%attr(755,root,root) %{_bindir}/em8300setup
/lib/firmware/em8300.bin
%dir %{_datadir}/em8300
%{_datadir}/em8300/em8300.pm
%attr(755,root,root) %{_datadir}/em8300/*.pl
%{_mandir}/man1/em8300setup.1*
%attr(754,root,root) /etc/rc.d/init.d/%{pname}
%config(noreplace) %verify(not md5 mtime size) /etc/sysconfig/%{pname}
# subpackage? (is it usable without alsa?)
%{_datadir}/alsa/cards/EM8300.conf

%files devel
%defattr(644,root,root,755)
%{_includedir}/linux/em8300.h

%files gtk
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/autocal
%attr(755,root,root) %{_bindir}/dhc
%attr(755,root,root) %{_bindir}/dxr3view
%endif

%if %{with kernel}
%if %{with up} || %{without dist_kernel}
%files -n kernel%{_alt_kernel}-video-em8300
%defattr(644,root,root,755)
/lib/modules/%{_kernel_ver}/kernel/drivers/video/*.ko*
%endif

%if %{with dist_kernel} && %{with smp}
%files -n kernel%{_alt_kernel}-smp-video-em8300
%defattr(644,root,root,755)
/lib/modules/%{_kernel_ver}smp/kernel/drivers/video/*.ko*
%endif
%endif
