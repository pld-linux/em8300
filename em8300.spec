Summary:	dxr3 and h+ driver
Summary(pl):	sterowniki dla dxr3 i h+
Name:		em8300
Version:	0.12.0
Release:	1
License:	GPL
Group:		Libraries
Source0:	http://dxr3.sourceforge.net/download/%{name}-%{version}.tar.gz
Source1:	%{name}.init
Source2:	%{name}.sysconf
URL:		http://dxr3.sourceforge.net/
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	libtool
BuildRequires:	gtk+-devel >= 1.2.0
Requires(post,postun):	/sbin/ldconfig
Requires(post,postun):	/sbin/depmod
Requires(post,preun):	/sbin/chkconfig
Provides:	dxr3
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_xbindir		%{_prefix}/X11R6/bin

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

%prep
%setup -q

%build
rm -f missing
sh bootstrap
%{__automake}
%configure
%{__make}
cd modules
make

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT

%{__make} install DESTDIR=$RPM_BUILD_ROOT
cd modules
%{__make} install-newkern prefix=$RPM_BUILD_ROOT
find $RPM_BUILD_ROOT/lib/modules -name "*.o" -print | sed s,$RPM_BUILD_ROOT,, >../mods.lst
mv INSTALL INSTALL.modules

install -D em8300.uc $RPM_BUILD_ROOT/%{_datadir}/misc/em8300.uc

cd $RPM_BUILD_ROOT
install -d ./%{_xbindir}
mv ./%{_bindir}/* ./%{_xbindir}

cd $RPM_BUILD_ROOT%{_datadir}
install -m 755 em8300/microcode_upload.pl ../bin/em8300_microcode_upload
install -D %{SOURCE1} $RPM_BUILD_ROOT/%{_sysconfdir}/rc.d/init.d/%{name}
install -D %{SOURCE2} $RPM_BUILD_ROOT/%{_sysconfdir}/sysconfig/%{name}

%clean
rm -rf $RPM_BUILD_ROOT $RPM_BUILD_DIR/%{name}-%{version}

%postun
/sbin/ldconfig
/sbin/depmod -a

%post
/sbin/ldconfig
/sbin/depmod -a
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

%files -f mods.lst
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog COPYING README 
%doc modules/{README*,INSTALL*,devices.sh,devfs_symlinks}
%attr(755,root,root) %{_bindir}/*
%attr(755,root,root) %{_datadir}/misc/*
%attr(755,root,root) %{_libdir}/lib*.so.*
%attr(755,root,root) %{_sysconfdir}/rc.d/init.d/%{name}
%attr(755,root,root) %config(noreplace) %verify(not size mtime md5) %{_sysconfdir}/sysconfig/%{name}

%files devel
%defattr(644,root,root,755)
%{_includedir}/libdxr3
%{_includedir}/linux/*
%attr(755,root,root) %{_libdir}/lib*.so
%attr(755,root,root) %{_libdir}/lib*.la
%attr(755,root,root) %dir %{_datadir}/em8300
%attr(755,root,root) %{_datadir}/em8300/*

%files static
%defattr(644,root,root,755)
%{_libdir}/*.a

%files gtk
%defattr(644,root,root,755)
%attr(755,root,root) %{_xbindir}/*
