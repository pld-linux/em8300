#
# Conditional build:
# _without_dist_kernel	- without distribution kernel
#
# TODO: UP/SMP modules
Summary:	dxr3 and h+ driver
Summary(pl):	sterowniki dla dxr3 i h+
Name:		em8300
Version:	0.13.0
Release:	1
License:	GPL
Group:		Libraries
Source0:	http://dxr3.sourceforge.net/download/%{name}-%{version}.tar.gz
# Source0-md5:	306984dfd4f0f29538179cbbf391f5a8
Source1:	%{name}.init
Source2:	%{name}.sysconf
Patch0:		%{name}-automake.patch
URL:		http://dxr3.sourceforge.net/
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	libtool
BuildRequires:	gtk+-devel >= 1.2.0
%{!?_without_dist_kernel:BuildRequires:	kernel-headers}
BuildRequires:	rpmbuild(macros) >= 1.118
Requires(post,postun):	/sbin/ldconfig
Requires(post,preun):	/sbin/chkconfig
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

%package devel
Summary:	Files required to develop programs using em8300
Summary(pl):	Pliki potrzebne do tworzenia programów korzystaj±cych z em8300
Group:		Development/Libraries
Requires:	%{name} = %{version}

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
Requires:	%{name}-devel = %{version}

%description static
Static libraries for em8300.

%description static -l pl
Statyczne biblioteki dla em8300.

%package gtk
Summary:	Utility programs for em8300 using gtk+
Summary(pl):	Programy u¿ytkowe em8300 u¿ywaj±ce bibliteki gtk+
Group:		X11/Applications
Requires:	%{name} = %{version}

%description gtk
Utility programs for em8300 using gtk+ toolkit.

%description gtk -l pl
Programy u¿ytkowe em8300 u¿ywaj±ce biblioteki gtk+.

%package -n kernel-video-em8300
Summary:	em8300 Linux kernel modules
Summary(pl):	Modu³y j±dra Linuksa em8300
Group:		Base/Kernel
%{!?_without_dist_kernel:%requires_releq_kernel_up}
Requires(post,postun):	/sbin/depmod

%description -n kernel-video-em8300
em8300 Linux kernel modules.

%description -n kernel-video-em8300 -l pl
Modu³y j±dra Linuksa em8300.

%prep
%setup -q
%patch0 -p1

%build
rm -f missing
%{__libtoolize}
%{__aclocal} -I autotools
%{__autoconf}
%{__autoheader}
%{__automake}
%configure
%{__make}

%{__make} -C modules \
	KERNEL_LOCATION="%{_kernelsrcdir}" \
	EM8300_DEBUG="%{rpmcflags}"

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

%{__make} -C modules install-newkern \
	KERNVER=%{_kernel_ver} \
	prefix=$RPM_BUILD_ROOT

mv -f modules/{INSTALL,INSTALL.modules}

install -D modules/em8300.uc $RPM_BUILD_ROOT%{_datadir}/misc/em8300.uc

install scripts/microcode_upload.pl $RPM_BUILD_ROOT%{_bindir}/em8300_microcode_upload

install -D %{SOURCE1} $RPM_BUILD_ROOT/etc/rc.d/init.d/%{name}
install -D %{SOURCE2} $RPM_BUILD_ROOT/etc/sysconfig/%{name}

%clean
rm -rf $RPM_BUILD_ROOT

%post
/sbin/ldconfig
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

%postun	-p /sbin/ldconfig

%post	-n kernel-video-em8300
%depmod %{_kernel_ver}
 
%postun	-n kernel-video-em8300
%depmod %{_kernel_ver}

%files
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog README modules/{README*,INSTALL*,devices.sh,devfs_symlinks}
%attr(755,root,root) %{_bindir}/em8300_microcode_upload
%{_datadir}/misc/em8300.uc
%attr(755,root,root) %{_libdir}/lib*.so.*.*.*
%attr(754,root,root) /etc/rc.d/init.d/%{name}
%config(noreplace) %verify(not size mtime md5) /etc/sysconfig/%{name}

%files devel
%defattr(644,root,root,755)
%{_includedir}/libdxr3
%{_includedir}/linux/*.h
%attr(755,root,root) %{_libdir}/lib*.so
%{_libdir}/lib*.la
%attr(755,root,root) %dir %{_datadir}/em8300
%attr(755,root,root) %{_datadir}/em8300/*

%files static
%defattr(644,root,root,755)
%{_libdir}/lib*.a

%files gtk
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/autocal
%attr(755,root,root) %{_bindir}/dhc
%attr(755,root,root) %{_bindir}/dxr3view
%attr(755,root,root) %{_bindir}/em8300setup

%files -n kernel-video-em8300
%defattr(644,root,root,755)
/lib/modules/%{_kernel_ver}/kernel/drivers/video/*.o*
