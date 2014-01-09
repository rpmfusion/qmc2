Name:           qmc2
Version:        0.42
Release:        1%{?dist}
Summary:        M.A.M.E./M.E.S.S./U.M.E. Catalog / Launcher II, common files

License:        GPLv2
URL:            http://qmc2.arcadehits.net/
Source0:        http://downloads.sourceforge.net/qmc2/%{name}-%{version}.tar.bz2
Patch1:         qmc2-ini.patch

BuildRequires:  desktop-file-utils
BuildRequires:  libXmu-devel
BuildRequires:  phonon-devel
BuildRequires:  qt4-webkit-devel
BuildRequires:  rsync
BuildRequires:  SDL-devel
Requires:       games-menus
Requires:       %{name}-binary%{?_isa} = %{version}-%{release}

%description
QMC2 is a Qt4 based UNIX frontend for MAME and MESS. This package
contains the common files.


%package sdlmame
Summary:        M.A.M.E. Catalog / Launcher II
Requires:       %{name}%{?_isa} = %{version}-%{release}
Requires:       mame
Provides:       %{name}-binary%{?_isa} = %{version}-%{release}

%description sdlmame
QMC2 is a Qt4 based UNIX frontend for MAME and MESS. This package
contains the parts required for MAME support.


%package sdlmess
Summary:        M.E.S.S. Catalog / Launcher II
Requires:       %{name}%{?_isa} = %{version}-%{release}
Requires:       mess
Provides:       %{name}-binary%{?_isa} = %{version}-%{release}

%description sdlmess
QMC2 is a Qt4 based UNIX frontend for MAME and MESS. This package
contains the parts required for MESS support.


%package -n qchdman
Summary:        Qt CHDMAN GUI
Requires:       mame-tools

%description -n qchdman
A stand-alone graphical user interface / front-end to chdman


%prep
%setup -qcT
tar -xjf %{SOURCE0}
mv %{name} sdlmame
ln -s Fedora.cfg sdlmame/arch/Linux/Fedora_release_21.cfg
tar -xjf %{SOURCE0}
mv %{name} sdlmess
ln -s Fedora.cfg sdlmess/arch/Linux/Fedora_release_21.cfg
%patch1 -p1 -b .ini
chmod 644 sdlmame/tools/qchdman/scriptwidget.*


%build
pushd sdlmess
make %{?_smp_mflags} CTIME=0 DISTCFG=1 EMULATOR=SDLMESS PRETTY=0 \
    PREFIX=%{_prefix} SYSCONFDIR=%{_sysconfdir}
popd

pushd sdlmame
make %{?_smp_mflags} CTIME=0 DISTCFG=1 EMULATOR=SDLMAME PRETTY=0 \
    PREFIX=%{_prefix} SYSCONFDIR=%{_sysconfdir}

make qchdman %{?_smp_mflags} CTIME=0 DISTCFG=1 PRETTY=0 \
    PREFIX=%{_prefix} SYSCONFDIR=%{_sysconfdir}
popd


%install
rm -rf $RPM_BUILD_ROOT

pushd sdlmess
make install DESTDIR=$RPM_BUILD_ROOT DISTCFG=1 \
    PRETTY=0 CTIME=0 PREFIX=%{_prefix} SYSCONFDIR=%{_sysconfdir} \
    EMULATOR=SDLMESS QT_TRANSLATION=../../qt4/translations
popd

#remove the qmc2.ini since we only need one
rm -f $RPM_BUILD_ROOT%{_sysconfdir}/qmc2/qmc2.ini

pushd sdlmame
make install DESTDIR=$RPM_BUILD_ROOT DISTCFG=1 \
    PRETTY=0 CTIME=0 PREFIX=%{_prefix} SYSCONFDIR=%{_sysconfdir} \
    EMULATOR=SDLMAME QT_TRANSLATION=../../qt4/translations

make qchdman-install DESTDIR=$RPM_BUILD_ROOT DISTCFG=1 \
    PRETTY=0 CTIME=0 PREFIX=%{_prefix} SYSCONFDIR=%{_sysconfdir} \
    QT_TRANSLATION=../../qt4/translations 
popd

#remove docs since we are installing docs in %%doc
pushd $RPM_BUILD_ROOT%{_datadir}/%{name}
rm -fr doc
ln -s ../doc/%{name}-%{version} doc
popd

#validate the desktop files
desktop-file-validate $RPM_BUILD_ROOT%{_datadir}/applications/qmc2-sdlmame.desktop
desktop-file-validate $RPM_BUILD_ROOT%{_datadir}/applications/qmc2-sdlmess.desktop
desktop-file-validate $RPM_BUILD_ROOT%{_datadir}/applications/qchdman.desktop


%files
%doc sdlmame/data/doc/html
%config(noreplace) %{_sysconfdir}/qmc2
%{_bindir}/runonce
%{_datadir}/qmc2


%files sdlmame
%{_bindir}/qmc2
%{_bindir}/qmc2-sdlmame
%{_datadir}/applications/qmc2-sdlmame.desktop


%files sdlmess
%{_bindir}/qmc2-sdlmess
%{_datadir}/applications/qmc2-sdlmess.desktop


%files -n qchdman
%{_bindir}/qchdman
%{_datadir}/applications/qchdman.desktop


%changelog
* Thu Jan 09 2014 Julian Sikorski <belegdol@fedoraproject.org> - 0.42-1
- Updated to 0.42

* Sun Nov 10 2013 Julian Sikorski <belegdol@fedoraproject.org> - 0.41-1
- Updated to 0.41

* Thu Sep 19 2013 Julian Sikorski <belegdol@fedoraproject.org> - 0.40-1
- Updated to 0.40
- cheat_file → cheatpath

* Mon Jun 17 2013 Julian Sikorski <belegdol@fedoraproject.org> - 0.39-1
- Updated to 0.39
- Added qchdman
- Fixed Source0 URL

* Sat Jan 12 2013 Julian Sikorski <belegdol@fedoraproject.org> - 0.38-1
- Updated to 0.38
- Updated the ini patch

* Fri Sep 21 2012 Julian Sikorski <belegdol@fedoraproject.org> - 0.37-1
- Updated to 0.37
- Updated the ini patch
- SDLMAME/SDLMESS have been gone for a while, so just use them internally
- Require mame/mess since the compatibility provides were dropped
- Updated summaries

* Tue May 22 2012 Julian Sikorski <belegdol@fedoraproject.org> - 0.36-1
- Updated to 0.36

* Thu Mar 08 2012 Nicolas Chauvet <kwizart@gmail.com> - 0.35-3
- Rebuilt for c++ ABI breakage

* Thu Feb 09 2012 Nicolas Chauvet <kwizart@gmail.com> - 0.35-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Mon Feb 06 2012 Julian Sikorski <belegdol@fedoraproject.org> - 0.35-1
- Updated to 0.35
- Updated the ini patch
- Made the inter-subpackage dependencies arch-specific

* Tue Nov 15 2011 Julian Sikorski <belegdol@fedoraproject.org> - 0.34-1
- Updated to 0.34 (new versioning scheme)
- Dropped obsolete Group, Buildroot, %%clean and %%defattr

* Wed Jun 29 2011 Julian Sikorski <belegdol@fedoraproject.org> - 0.2-0.24.b20
- Updated to 0.2b20
- Updated the ini patch

* Sun Apr 03 2011 Julian Sikorski <belegdol@fedoraproject.org> - 0.2-0.23.b19
- Updated to 0.2b19

* Thu Jan 13 2011 Julian Sikorski <belegdol@fedoraproject.org> - 0.2-0.22.b18
- Updated to 0.2b18

* Fri Oct 22 2010 Julian Sikorski <belegdol@fedoraproject.org> - 0.2-0.21.b17
- Updated to 0.2b17
- Added Fedora 15 config

* Fri Jul 30 2010 Julian Sikorski <belegdol@fedoraproject.org> - 0.2-0.20.b16
- Updated to 0.2b16

* Sun May 16 2010 Julian Sikorski <belegdol@fedoraproject.org> - 0.2-0.19.b15
- Updated to 0.2b15
- Updated the ini template patch to include Catver.ini
- s/qt4-devel/qt-webkit-devel due to changes in qt package

* Mon Mar 15 2010 Julian Sikorski <belegdol[at]gmail[dot]com> - 0.2-0.18.b14
- Updated to 0.2b14
- Dropped --fno-var-tracking-assignments

* Sat Jan 02 2010 Julian Sikorski <belegdol[at]gmail[dot]com> - 0.2-0.17.b13
- Updated to 0.2b13
- Dropped the cflags patch
- Dropped the additional Fedora configs

* Sat Nov 21 2009 Julian Sikorski <belegdol[at]gmail[dot]com> - 0.2-0.16.b12
- Updated to 0.2b12
- Worked around RH bug 532763 for Fedora 12 and above
- Added Fedora 12 and Fedora 13 configs

* Fri Sep 11 2009 Julian Sikorski <belegdol[at]gmail[dot]com> - 0.2-0.15.b11
- Updated to 0.2b11
- Updated the ini patch
- Dropped F12 rawhide workaround

* Mon Jul 20 2009 Julian Sikorski <belegdol[at]gmail[dot]com> - 0.2-0.14.b10
- Updated to 0.2b10
- Added F12 rawhide config

* Mon Jun 08 2009 Julian Sikorski <belegdol[at]gmail[dot]com> - 0.2-0.13.b9
- Updated to 0.2b9

* Thu Apr 23 2009 Julian Sikorski <belegdol[at]gmail[dot]com> - 0.2-0.12.b8
- Updated to 0.2b8
- Updated the ini patch
- Dropped the upstreamed gcc44 patch
- Dropped the F11 Beta workaround

* Mon Mar 30 2009 Julian Sikorski <belegdol[at]gmail[dot]com> - 0.2-0.11.b7
- Handle the template properly
- Updated the configs for Fedora 11 Beta

* Sun Mar 29 2009 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 0.2-0.10.b7
- rebuild for new F11 features

* Mon Mar 09 2009 Julian Sikorski <belegdol[at]gmail[dot]com> - 0.2-0.9.b7
- Updated to 0.2b7
- Dropped the rawhide fedora-release workaround
- Overhauled for sdlmess support
- Desktop files now come with the tarball and use the shipped icon
- Updated Summary and %%description (M.A.M.E. → M.A.M.E./M.E.S.S.)
- Updated the ini patch
- Avoid installing qmc2.ini.new
- Dropped hicolor-icon-theme from Requires
- Switched to system-wide Qt translations
- No longer force Windows Qt style
- Updated the URL
- Added libXmu-devel to BuildRequires
- Added gcc-4.4 fix from SVN

* Mon Jan  5 2009 Julian Sikorski <belegdol[at]gmail[dot]com> - 0.2-0.8.b6
- Updated to 0.2b6
- Updated the ini patch
- Updated the rawhide fedora-relase workaround
- Added PRETTY=0 to compilation flags

* Thu Oct 16 2008 Julian Sikorski <belegdol[at]gmail[dot]com> - 0.2-0.7.b5
- Updated to 0.2b5

* Tue Aug 19 2008 Julian Sikorski <belegdol[at]gmail[dot]com> - 0.2-0.6.b4
- Added phonon-devel to BuildRequires
- Cleaned up BuildRequires and Requires

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
