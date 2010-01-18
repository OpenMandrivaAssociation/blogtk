%define version	2.0
%define release %mkrel 3
%define newname blogtk2

Name:		blogtk
Summary:	Standalone blog entry poster
Version:	%{version}
Release:	%{release}
Source:		http://launchpad.net/blogtk/2.0/2.0/+download/%{name}-%{version}.tar.gz
URL:		http://blogtk.jayreding.com
License:	Apache License
Group:		Networking/Other
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot
BuildRequires:	imagemagick
BuildRequires:	desktop-file-utils
Requires:	pygtk2.0
Requires:	pygtk2.0-libglade
Requires:	gnome-python
Requires:	gnome-python-gtkspell
Requires:	python-webkitgtk
Requires:	python-gdata
Requires:	python-gtksourceview
Requires:	python-feedparser
Requires(pre):	desktop-file-utils
BuildArch:	noarch

%description
BloGTK is a weblog client that allows you to post to your weblog from Linux
without the need for a separate browser window. BloGTK allows you to connect
with many weblog systems such as Blogger, Movable Type, WordPress, and more.

%prep
%setup -q -n %name-%version

chmod 644 data/*

# (Abel) eliminate runtime pygtk warnings
find -type f -name '*.py' -print0 | xargs -r -0 perl -pi -e 's/gtk\.TRUE/True/g; s/gtk\.FALSE/False/g;'

%install
rm -rf %{buildroot}
mkdir -p %{buildroot}%{_datadir}
cp -r share/blogtk2 %{buildroot}%{_datadir}
mkdir -p %{buildroot}/%{_datadir}/pixmaps
cp data/blogtk-icon.png %{buildroot}/%{_datadir}/pixmaps
mkdir -p %{buildroot}/%{_datadir}/applications
cp data/blogtk.desktop %{buildroot}/%{_datadir}/applications/
mkdir -p %{buildroot}/%{_bindir}
cp bin/blogtk2 %{buildroot}/%{_bindir}/

#menu
perl -pi -e 's,blogtk-icon.png,%{name},g' %{buildroot}%{_datadir}/applications/*
desktop-file-install --remove-category="Application" \
  --add-category="GTK" \
  --remove-key=Encoding \
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
%{_bindir}/%{newname}
%{_datadir}/%{newname}
%{_datadir}/pixmaps/*
%{_datadir}/applications/*
%{_iconsdir}/hicolor/*/apps/%{name}.png
