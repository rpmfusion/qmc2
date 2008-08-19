%define beta b4

Name:           qmc2
Version:        0.2
Release:        0.5.%{beta}%{?dist}
Summary:        M.A.M.E. Catalog / Launcher II

Group:          Applications/Emulators
License:        GPLv2
URL:            http://www.mameworld.net/mamecat
Source0:        http://dl.sourceforge.net/qmc2/%{name}-%{version}.%{beta}.tar.bz2
Source1:        %{name}.png
Patch1:         qmc2-ini.patch
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:  desktop-file-utils, rsync, qt4-devel >= 4.2.2
BuildRequires:  SDL-devel
Requires:       hicolor-icon-theme, dribble-menus, sdlmame

%description
QMC2 is a Qt4 based UNIX MAME frontend supporting both XMAME and SDLMAME.


%prep
%setup -qn %{name}
%patch1 -p0 -b .ini~

# create qmc2 desktop file
cat > %{name}.desktop << EOF
[Desktop Entry]
Encoding=UTF-8
Name=%{name}
GenericName=M.A.M.E. Catalog / Launcher II
Comment=SDL MAME Frontend
Exec=%{name}
Icon=%{name}.png
Terminal=false
Type=Application
Categories=Game;Emulator;
EOF


%build
QTDIR=%{_prefix} make %{?_smp_mflags} CTIME=0 DISTCFG=1\
    PREFIX=%{_prefix} SYSCONFDIR=%{_sysconfdir}


%install
rm -rf $RPM_BUILD_ROOT
QTDIR=%{_prefix} make install DESTDIR=$RPM_BUILD_ROOT DISTCFG=1\
    CTIME=0 PREFIX=%{_prefix} SYSCONFDIR=%{_sysconfdir}

# remove docs since we are intalling docs in %doc
pushd $RPM_BUILD_ROOT%{_datadir}/%{name}
rm -fr doc
ln -s ../doc/%{name}-%{version} doc
popd

# install fedora desktop file
desktop-file-install --vendor=dribble \
    --dir=$RPM_BUILD_ROOT%{_datadir}/applications \
    %{name}.desktop

# install icon
install -d $RPM_BUILD_ROOT%{_datadir}/icons/hicolor/64x64/apps
install -pm 644 %{SOURCE1} $RPM_BUILD_ROOT%{_datadir}/icons/hicolor/64x64/apps

#fix the executable permissions
chmod 755 $RPM_BUILD_ROOT%{_bindir}/%{name}


%post
touch --no-create %{_datadir}/icons/hicolor || :
%{_bindir}/gtk-update-icon-cache --quiet %{_datadir}/icons/hicolor || :

%postun
touch --no-create %{_datadir}/icons/hicolor || :
%{_bindir}/gtk-update-icon-cache --quiet %{_datadir}/icons/hicolor || :


%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr(-,root,root,-)
%doc data/doc/html
%config(noreplace) %{_sysconfdir}/%{name}
%{_bindir}/%{name}
%{_datadir}/%{name}
%{_datadir}/icons/hicolor/64x64/apps/%{name}.png
%{_datadir}/applications/*.desktop


%changelog
* Tue Aug 19 2008 Julian Sikorski <belegdol[at]gmail[dot]com> - 0.2-0.5.b4
- Updated to 0.2b4

* Wed Jul 30 2008 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info - 0.2-0.4.b3
- rebuild for buildsys cflags issue

* Mon Jul  7 2008 Julian Sikorski <belegdol[at]gmail[dot]com> - 0.2-0.3.b3
- Updated to 0.2b3
- Dropped the qt4 patch, use DISTCFG instead
- Updated the ini patch to include dat files location
- Added SDL-devel to BuildRequires

* Sat May 10 2008 Julian Sikorski <belegdol[at]gmail[dot]com> - 0.2-0.2.b2
- Updated to 0.2b2
- Dropped %%{?dist} from %%changelog
- Added hyphen before version number in %%changelog

* Wed Mar 26 2008 Julian Sikorski <belegdol[at]gmail[dot]com> - 0.2-0.1.b1
- Updated to 0.2b1
- Dropped the ini fix since it has been merged upstream

* Sat Feb 23 2008 Julian Sikorski <belegdol[at]gmail[dot]com> - 0.1-4
- Updated the inipaths to reflect the post-0.123u1 SDLMAME configuration

* Sat Feb 23 2008 Julian Sikorski <belegdol[at]gmail[dot]com> - 0.1-3
- Replaced the previous workaround with a proper fix from upstream

* Mon Feb 11 2008 Julian Sikorski <belegdol[at]gmail[dot]com> - 0.1-2
- Updated the ini path to fix import/export feature

* Wed Feb  6 2008 Julian Sikorski <belegdol[at]gmail[dot]com> - 0.1-1
- Upstream sync

* Thu Jan 31 2008 Julian Sikorski <belegdol[at]gmail[dot]com> - 0.1-0.10.b11
- Upstream sync
- Drop backup files deletion, there are none present
- Adjusted the License tag
- Fixed the executable permissions

* Mon Jul 30 2007 XulChris <tkmame@retrogames.com> - 0.1-0.9.b10
- Upstream sync
- Remove no longer needed qt43 patch

* Mon Jul 02 2007 XulChris <tkmame@retrogames.com> - 0.1-0.8.b9
- Add patch to fix Qt-4.3 segmentation fault

* Sun Apr 22 2007 XulChris <tkmame@retrogames.com> - 0.1-0.7.b9
- Remove style from desktop file and add it to ini file instead
- Dribble Bugzilla #89

* Fri Mar 30 2007 XulChris <tkmame@retrogames.com> - 0.1-0.6.b9
- Upstream sync
- Remove no longer needed datadir patch

* Sun Mar 11 2007 XulChris <tkmame@retrogames.com> - 0.1-0.5.b8
- Update desktop category
- Include new paths in ini file
- Add patch to fix DATADIR parsing in Makefile

* Fri Feb 23 2007 XulChris <tkmame@retrogames.com> - 0.1-0.4.b8
- Upstream sync
- Update Source0 URL
- Remove patches which are now included in upstream
- Move creation of desktop file to %%prep
- Sync ini patch with new ini template

* Wed Jan 31 2007 XulChris <tkmame@retrogames.com> - 0.1-0.3.b7
- Fix ini patch

* Wed Jan 17 2007 XulChris <tkmame@retrogames.com> - 0.1-0.2.b7
- Make opengl default video mode
- Remove macros from Patch tags
- Move creation of .desktop file into %%build
- Fix Categories field in .desktop file
- Remove Version field from .desktop file
- Fix documentation

* Sun Dec 24 2006 XulChris <tkmame@retrogames.com> - 0.1-0.1.b7
- Initial Release
