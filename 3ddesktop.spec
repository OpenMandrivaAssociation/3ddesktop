%define	name	3ddesktop
%define	version	0.2.9
%define	cvsrel	cvs20040615
%define	rel	3
%define	release	%mkrel %{rel}
%define	Summary	OpenGL virtual desktop switcher

Summary:	%{Summary}
Name:		%{name}
Version:	%{version}
Release:	%{release}
License:	GPL
Group:		Graphical desktop/Other
Source0:	%{name}-%{version}.tar.bz2
Source11:	%{name}-16x16.png
Source12:	%{name}-32x32.png
Source13:	%{name}-48x48.png
#This might not be the best way, but..
Source2:	%{name}.sh.bz2
Patch0:		3ddesktop-0.2.9-x86_64.patch.bz2
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
CXXFLAGS="$RPM_OPT_FLAGS -O3" \
%configure2_5x	--sysconfdir=%{_sysconfdir}/X11 \
		--disable-dependency-tracking \
		--with-qt-dir=%{_prefix}/lib/qt3 \
		--with-kde-includes=%{_includedir}

%make

%install
rm -rf $RPM_BUILD_ROOT
%{makeinstall_std}
bzcat %{SOURCE2} > $RPM_BUILD_ROOT%{_bindir}/%{name}; chmod 755 $RPM_BUILD_ROOT%{_bindir}/%{name}

install -d $RPM_BUILD_ROOT%{_menudir}
cat <<EOF >$RPM_BUILD_ROOT%{_menudir}/%{name}
?package(%{name}):command="%{_bindir}/%{name}" \
		  icon=%{name}.png \
		  needs="x11" \
		  section="Amusement/Toys" \
		  title="3d-Desktop"\
		  longtitle="%{Summary}"
EOF

install -m644 %{SOURCE11} -D $RPM_BUILD_ROOT%{_miconsdir}/%{name}.png
install -m644 %{SOURCE12} -D $RPM_BUILD_ROOT%{_iconsdir}/%{name}.png
install -m644 %{SOURCE13} -D $RPM_BUILD_ROOT%{_liconsdir}/%{name}.png

%post
%{update_menus}

%postun
%{clean_menus}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root)
%doc README ChangeLog TODO AUTHORS
%{_bindir}/*
%dir %{_datadir}/%{name}
%{_datadir}/%{name}/digits.bmp
%{_mandir}/man1/*.1*
%{_menudir}/%{name}
%{_iconsdir}/%{name}.png
%{_liconsdir}/%{name}.png
%{_miconsdir}/%{name}.png
%config(noreplace) %{_sysconfdir}/X11/%{name}.conf

