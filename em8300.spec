Summary:	dxr3 and h+ driver
Summary(pl):	sterowniki dla dxr3 i h+
Name:		em8300
Version:	0.12
Release:	0
License:	GPL
Group:		Base/Kernel
Source0:	http://dxr3.sourceforge.net/download/%{name}-%{version}.tar.gz
URL:		http://dxr3.sourceforge.net/
Provides:	dxr3
BuildRequires:	kernel-headers
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description

em8300 is a Linux driver for Creative DXR3 and Sigma Designs Hollywood+
cards. Both cards are hardware MPEG1, MPEG2, AC3 decoders. Additionaly
Xine and MPlayer with help of this driver allow you to play all
the video formats that they recognise through the tv-out of these cards.

%description -l pl

em8300 pozwala na uruchomienie pod Linuksem kart Creative DXR3
i Sigma Designs Hollywood+. Obie karty, o prawie identycznej konstrukcji
s± sprzêtowymi dekoderami MPEG1, MPEG2 i AC3. Programy Xine i MPlayer
pozwalaj± przy u¿yciu tego sterownika na odtwarzanie przez wyj¶cie
telewizyjne tych kart nie tylko w/w formatów, ale tak¿e wszystkich
formatów video, które te programy rozpoznaj±.

%prep
%setup -q

%build
%configure
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT

%{__make} install DESTDIR=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%preun

%post

%files
%defattr(644,root,root,755)
%doc *.gz
%attr(755,root,root) %{_bindir}/*
%{_datadir}/%{name}
