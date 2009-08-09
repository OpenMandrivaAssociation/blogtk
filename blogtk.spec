%define version	1.1
%define release %mkrel 9

Name: 	 	blogtk
Summary: 	Standalone blog entry poster
Version: 	%{version}
Release: 	%{release}

Source:		http://kent.dl.sourceforge.net/sourceforge/blogtk/%{name}_%{version}.tar.bz2
URL:		http://blogtk.sourceforge.net/
License:	BSD
Group:		Networking/Other
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot
BuildRequires:	imagemagick
BuildRequires:	desktop-file-utils
Requires:	pygtk2.0 
Requires:       pygtk2.0-libglade 
Requires:       gnome-python-gtkhtml2 
Requires:       gnome-python
Requires(pre):  desktop-file-utils
BuildArch:	noarch

%description
BloGTK is a weblog client that allows you to post to your weblog from Linux
without the need for a separate browser window. BloGTK allows you to connect
with many weblog systems such as Blogger, Movable Type, WordPress, and more.

%prep
%setup -q -n BloGTK-%version

chmod 644 data/* pixmaps/*
chmod 755 src/BloGTK.py

# (Abel) eliminate runtime pygtk warnings
find -type f -name '*.py' -print0 | xargs -r -0 perl -pi -e 's/gtk\.TRUE/True/g; s/gtk\.FALSE/False/g;'

%install
rm -rf %{buildroot}
mkdir -p %{buildroot}/%{_datadir}/%{name}
cp src/* %{buildroot}/%{_datadir}/%{name}
cp pixmaps/* %{buildroot}/%{_datadir}/%{name}
mkdir -p %{buildroot}/%{_datadir}/pixmaps
cp data/blogtk-icon.png %{buildroot}/%{_datadir}/pixmaps
mkdir -p %{buildroot}/%{_datadir}/applications
cp data/blogtk.desktop %{buildroot}/%{_datadir}/applications/
mkdir -p %{buildroot}/%{_bindir}
ln -s %{_datadir}/%{name}/BloGTK.py %{buildroot}/%{_bindir}/%{name}

#menu

perl -pi -e 's,Exec=BloGTK,Exec=%{_bindir}/%{name},g' %{buildroot}%{_datadir}/applications/*
perl -pi -e 's,blogtk-icon.png,%{name},g' %{buildroot}%{_datadir}/applications/*
desktop-file-install --vendor="" \
  --remove-category="Application" \
  --add-category="GTK" \
  --dir %{buildroot}%{_datadir}/applications %{buildroot}%{_datadir}/applications/*

#icons
mkdir -p %{buildroot}%{_iconsdir}/hicolor/{16x16,32x32,48x48,128x128}/apps
install -m 644 data/%{name}-icon.png %{buildroot}%{_iconsdir}/hicolor/128x128/apps/%{name}.png
convert -scale 48 data/%{name}-icon.png %{buildroot}%{_iconsdir}/hicolor/48x48/apps/%{name}.png
convert -scale 32 data/%{name}-icon.png %{buildroot}%{_iconsdir}/hicolor/32x32/apps/%{name}.png
convert -scale 16 data/%{name}-icon.png %{buildroot}%{_iconsdir}/hicolor/16x16/apps/%{name}.png

%clean
rm -rf %{buildroot}

%if %mdkversion < 200900
%post
%{update_menus}
%{update_icon_cache hicolor}
%endif
		
%if %mdkversion < 200900
%postun
%{clean_menus}
%{clean_icon_cache hicolor}
%endif

%files
%defattr(-,root,root)
%doc README ChangeLog AUTHORS
%{_bindir}/%{name}
%{_datadir}/%{name}
%{_datadir}/pixmaps/*
%{_datadir}/applications/*
%{_iconsdir}/hicolor/*/apps/%{name}.png

