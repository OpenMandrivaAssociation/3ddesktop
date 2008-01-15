Summary:	OpenGL virtual desktop switcher
Name:		3ddesktop
Version:	0.2.9
Release:	%mkrel 4
License:	GPLv2+
Group:		Graphical desktop/Other
Source0:	%{name}-%{version}.tar.bz2
Source11:	%{name}-16x16.png
Source12:	%{name}-32x32.png
Source13:	%{name}-48x48.png
#This might not be the best way, but..
Source2:	%{name}.sh.bz2
Patch0:		3ddesktop-0.2.9-x86_64.patch
URL:		http://desk3d.sourceforge.net/
Requires:	imlib2 >= 1.0.2
BuildRequires:	imlib2-devel >= 1.0.2 
BuildRequires:  freetype-devel 
BuildRequires:  kdelibs-devel 
BuildRequires:  MesaGLU-devel 
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot

%description 
3d Destkop is an OpenGL program for switching virtual desktops in a
seamless 3-dimensional manner. The current desktop is mapped into a 3D
space where you may choose other screens. When activated the current
desktop appears to zoom out into the 3D view.  Several different
visualization modes are available.
You might want to add a keybinding in your window manager for this one.

%prep
%setup -q
%patch0 -p0

%build
./autogen.sh
CXXFLAGS="%{optflags} -O3" \
%configure2_5x	--sysconfdir=%{_sysconfdir}/X11 \
		--disable-dependency-tracking \
		--with-qt-dir=%{_prefix}/lib/qt3 \
		--with-kde-includes=%{_includedir}

%make

%install
rm -rf %{buildroot}
%{makeinstall_std}
bzcat %{SOURCE2} > %{buildroot}%{_bindir}/%{name}; chmod 755 %{buildroot}%{_bindir}/%{name}

mkdir -p %{buildroot}%{_datadir}/applications
cat > %{buildroot}%{_datadir}/applications/mandriva-%{name}.desktop <<EOF
[Desktop Entry]
Name=3DDesktop
Comment=OpenGL-based 3D desktop switcher
Exec=%{_bindir}/%{name} 
Icon=%{name}
Terminal=false
Type=Application
StartupNotify=true
Categories=Amusement;
EOF


install -m644 %{SOURCE11} -D %{buildroot}%{_iconsdir}/hicolor/16x16/apps/%{name}.png
install -m644 %{SOURCE12} -D %{buildroot}%{_iconsdir}/hicolor/32x32/apps/%{name}.png
install -m644 %{SOURCE13} -D %{buildroot}%{_iconsdir}/hicolor/48x48/apps/%{name}.png

%post
%{update_menus}
%{update_icon_cache hicolor}

%postun
%{clean_menus}
%{clean_icon_cache hicolor}

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root)
%doc README ChangeLog TODO AUTHORS
%{_bindir}/*
%{_datadir}/%{name}
%{_mandir}/man1/*.1*
%{_datadir}/applications/mandriva-%{name}.desktop
%{_iconsdir}/hicolor/*/apps/%{name}.png
%config(noreplace) %{_sysconfdir}/X11/%{name}.conf

