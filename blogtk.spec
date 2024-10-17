%define version	2.0
%define release 5
%define newname blogtk2

Name:		blogtk
Summary:	Standalone blog entry poster
Version:	%{version}
Release:	%{release}
Source:		http://launchpad.net/blogtk/2.0/2.0/+download/%{name}-%{version}.tar.gz
URL:		https://blogtk.jayreding.com
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


%changelog
* Sun Dec 05 2010 Oden Eriksson <oeriksson@mandriva.com> 2.0-4mdv2011.0
+ Revision: 610078
- rebuild

* Mon Jan 18 2010 Ahmad Samir <ahmadsamir@mandriva.org> 2.0-3mdv2010.1
+ Revision: 493194
- add missing BR (spotted by QA)

* Sun Jan 17 2010 Ahmad Samir <ahmadsamir@mandriva.org> 2.0-2mdv2010.1
+ Revision: 492773
- bump release (to ease upgrades in the future)

* Mon Dec 28 2009 Ahmad Samir <ahmadsamir@mandriva.org> 2.0-1mdv2010.1
+ Revision: 482960
- Update to 2.0
- Change URL and Source (now hosted on launchpad)
- Change License
- Clean spec

* Sun Aug 09 2009 Oden Eriksson <oeriksson@mandriva.com> 1.1-9mdv2010.0
+ Revision: 413174
- rebuild

* Thu Dec 11 2008 Oden Eriksson <oeriksson@mandriva.com> 1.1-8mdv2009.1
+ Revision: 312912
- lowercase ImageMagick

* Thu Jun 12 2008 Pixel <pixel@mandriva.com> 1.1-8mdv2009.0
+ Revision: 218438
- rpm filetriggers deprecates update_menus/update_scrollkeeper/update_mime_database/update_icon_cache/update_desktop_database/post_install_gconf_schemas

  + Thierry Vignaud <tv@mandriva.org>
    - rebuild
    - kill re-definition of %%buildroot on Pixel's request

  + Olivier Blin <oblin@mandriva.com>
    - restore BuildRoot

* Sat Sep 08 2007 Adam Williamson <awilliamson@mandriva.org> 1.1-7mdv2008.0
+ Revision: 82340
- rebuild for 2008
- fd.o icons
- correct errors in .desktop file
- drop legacy menu and icons
- drop patch, do it with a perl substitution instead
- spec clean


* Tue Oct 31 2006 Christiaan Welvaart <cjw@daneel.dyndns.org>
+ 2006-10-31 22:48:20 (74823)
- add BuildRequires: desktop-file-utils

* Tue Oct 31 2006 Christiaan Welvaart <cjw@daneel.dyndns.org>
+ 2006-10-31 22:45:29 (74822)
Import blogtk

* Thu Sep 28 2006 Lenny Cartier <lenny@mandriva.com> 1.1-5mdv2007.1
- fix xdg menu

* Wed Sep 13 2006 Nicolas Lécureuil <neoclust@mandriva.org> 1.1-4mdv2007.0
- XDG

* Fri Nov 11 2005 Abel Cheung <deaddog@mandriva.org> 1.1-3mdk
- Eliminate pygtk runtime warnings

* Wed Aug 10 2005 Austin Acton <austin@mandriva.org> 1.1-2mdk
- requires gnome-python

* Fri Feb 04 2005 Austin Acton <austin@mandrake.org> 1.1-1mdk
- initial package

