Summary:	dxr3 and h+ driver
Summary(pl):	sterowniki dla dxr3 i h+
Name:		em8300
Version:	0.12.0
Release:	0
License:	GPL
Group:		Base/Kernel
Source0:	http://dxr3.sourceforge.net/download/%{name}-%{version}.tar.gz
URL:		http://dxr3.sourceforge.net/
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	libtool
BuildRequires:	gtk+-devel
Requires(post,postun):/sbin/ldconfig
Requires(post,postun):/sbin/depmod
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
Designs Hollywood+. Obie karty, o prawie identycznej konstrukcji s�
sprz�towymi dekoderami MPEG1, MPEG2 i AC3. Programy Xine i MPlayer
pozwalaj� przy u�yciu tego sterownika na odtwarzanie przez wyj�cie
telewizyjne tych kart nie tylko w/w format�w, ale tak�e wszystkich
format�w video, kt�re te programy rozpoznaj�.

%package devel
Summary:	Files required to develop programs using em8300
Summary(pl):	Pliki potrzebne do tworzenia program�w korzystaj�cych z em8300
Group:		Base/Kernel
Requires:	%{name} = %{version}

%description devel
Header files and additional scripts useful for developers of em8300
apps.

%description devel -l pl
Pliki nag��wkowe i skrypty przydatne dla autor�w aplikacji
korzystaj�cych z em8300.

%package gtk
Summary:	Utility programs for em8300 using gtk+
Summary(pl):	Programy u�ytkowe em8300 u�ywaj�ce bibliteki gtk+
Group:		Base/Kernel
Requires:	%{name} = %{version}

%description gtk
Utility programs for em8300 using gtk+ toolkit.

%description gtk -l pl
Programy u�ytkowe em8300 u�ywaj�ce biblioteki gtk+.

%prep
%setup -q

%build
sh bootstrap
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

install -d $RPM_BUILD_ROOT/%{_datadir}/misc
install em8300.uc $RPM_BUILD_ROOT/%{_datadir}/misc

cd $RPM_BUILD_ROOT
install -d ./%{_xbindir}
mv ./%{_bindir}/* ./%{_xbindir}

cd $RPM_BUILD_ROOT%{_datadir}
install -m 755 em8300/microcode_upload.pl ../bin/em8300_microcode_upload

%clean
rm -rf $RPM_BUILD_ROOT $RPM_BUILD_DIR/%{name}-%{version}

%postun
/sbin/ldconfig
/sbin/depmod -a

%post
/sbin/ldconfig
/sbin/depmod -a

%files -f mods.lst
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog COPYING README
%doc modules/README* modules/INSTALL* modules/devices.sh modules/devfs_symlinks
%attr(755,root,root) %{_bindir}/*
%attr(755,root,root) %{_datadir}/misc/*
%attr(755,root,root) %{_libdir}/lib*.so.*

%files devel
%defattr(644,root,root,755)
%{_includedir}/libdxr3
%{_includedir}/linux/*
%attr(755,root,root) %{_libdir}/lib*.so
%attr(755,root,root) %{_libdir}/lib*.la
%attr(755,root,root) %dir %{_datadir}/em8300
%attr(755,root,root) %{_datadir}/em8300/*

%files gtk
%defattr(644,root,root,755)
%attr(755,root,root) %{_xbindir}/*
