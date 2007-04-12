%define version	1.1
%define release %mkrel 6

Name: 	 	blogtk
Summary: 	Standalone blog entry poster
Version: 	%{version}
Release: 	%{release}

Source:		http://kent.dl.sourceforge.net/sourceforge/blogtk/%{name}_%{version}.tar.bz2
Patch:		%name-desktop_file.patch
URL:		http://blogtk.sourceforge.net/
License:	BSD
Group:		Networking/Other
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot
BuildRequires:	ImageMagick
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

%patch -p 1

chmod 644 data/* pixmaps/*
chmod 755 src/BloGTK.py

# (Abel) eliminate runtime pygtk warnings
find -type f -name '*.py' -print0 | xargs -r -0 perl -pi -e 's/gtk\.TRUE/True/g; s/gtk\.FALSE/False/g;'

%install
rm -rf $RPM_BUILD_ROOT
mkdir -p %buildroot/%_datadir/%name
cp src/* %buildroot/%_datadir/%name
cp pixmaps/* %buildroot/%_datadir/%name
mkdir -p %buildroot/%_datadir/pixmaps
cp data/blogtk-icon.png %buildroot/%_datadir/pixmaps
mkdir -p %buildroot/%_datadir/applications
cp data/blogtk.desktop %buildroot/%_datadir/applications/
mkdir -p %buildroot/%_bindir
ln -s %_datadir/%name/BloGTK.py %buildroot/%_bindir/%name

#menu
mkdir -p $RPM_BUILD_ROOT%{_menudir}
cat << EOF > $RPM_BUILD_ROOT%{_menudir}/%{name}
?package(%{name}): command="%{name}" icon="%{name}.png" needs="x11" title="BloGTK" longtitle="Blog entry poster" section="Internet/Other" xdg="true"
EOF

desktop-file-install --vendor="" \
  --remove-category="Application" \
  --add-category="GTK" \
  --add-category="GNOME" \
  --add-category="X-MandrivaLinux-Internet-Other" \
  --add-category="Network" \
  --dir $RPM_BUILD_ROOT%{_datadir}/applications $RPM_BUILD_ROOT%{_datadir}/applications/*

#icons
mkdir -p $RPM_BUILD_ROOT/%_liconsdir
convert -size 48x48 data/%name-icon.png $RPM_BUILD_ROOT/%_liconsdir/%name.png
mkdir -p $RPM_BUILD_ROOT/%_iconsdir
convert -size 32x32 data/%name-icon.png $RPM_BUILD_ROOT/%_iconsdir/%name.png
mkdir -p $RPM_BUILD_ROOT/%_miconsdir
convert -size 16x16 data/%name-icon.png $RPM_BUILD_ROOT/%_miconsdir/%name.png

%clean
rm -rf $RPM_BUILD_ROOT

%post
%update_menus
		
%postun
%clean_menus

%files
%defattr(-,root,root)
%doc README ChangeLog AUTHORS
%{_bindir}/%name
%{_datadir}/%name
%{_datadir}/pixmaps/*
%{_datadir}/applications/*
%{_menudir}/%name
%{_liconsdir}/%name.png
%{_iconsdir}/%name.png
%{_miconsdir}/%name.png

