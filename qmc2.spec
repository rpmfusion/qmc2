%define beta b10

Name:           qmc2
Version:        0.2
Release:        0.14.%{beta}%{?dist}
Summary:        M.A.M.E./M.E.S.S. Catalog / Launcher II, common files

Group:          Applications/Emulators
License:        GPLv2
URL:            http://qmc2.arcadehits.net/
Source0:        http://dl.sourceforge.net/qmc2/%{name}-%{version}.%{beta}.tar.bz2
Patch1:         qmc2-ini.patch
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:  desktop-file-utils
BuildRequires:  libXmu-devel
BuildRequires:  phonon-devel
BuildRequires:  qt4-devel
BuildRequires:  rsync
BuildRequires:  SDL-devel
Requires:       games-menus
Requires:       %{name}-binary = %{version}-%{release}

%description
QMC2 is a Qt4 based UNIX frontend for SDLMAME and SDLMESS. This package
contains the common files.


%package sdlmame
Summary:        M.A.M.E./M.E.S.S. Catalog / Launcher II, SDLMAME support
Group:          Applications/Emulators
Requires:       %{name} = %{version}-%{release}
Requires:       sdlmame
Provides:       %{name}-binary = %{version}-%{release}

%description sdlmame
QMC2 is a Qt4 based UNIX frontend for SDLMAME and SDLMESS. This package
contains the parts required for SDLMAME support.


%package sdlmess
Summary:        M.A.M.E./M.E.S.S. Catalog / Launcher II, SDLMESS support
Group:          Applications/Emulators
Requires:       %{name} = %{version}-%{release}
Requires:       sdlmess
Provides:       %{name}-binary = %{version}-%{release}

%description sdlmess
QMC2 is a Qt4 based UNIX frontend for SDLMAME and SDLMESS. This package
contains the parts required for SDLMESS support.


%prep
%setup -qcT
tar -xjf %{SOURCE0}
mv %{name} sdlmame
tar -xjf %{SOURCE0}
mv %{name} sdlmess

pushd sdlmess
%patch1 -p0 -b .ini~
popd

pushd sdlmame
%patch1 -p0 -b .ini~
popd


%build
pushd sdlmess
QTDIR=%{_prefix} make %{?_smp_mflags} CTIME=0 DISTCFG=1\
    PRETTY=0 PREFIX=%{_prefix} SYSCONFDIR=%{_sysconfdir} \
    EMULATOR=SDLMESS
popd

pushd sdlmame
QTDIR=%{_prefix} make %{?_smp_mflags} CTIME=0 DISTCFG=1\
    PRETTY=0 PREFIX=%{_prefix} SYSCONFDIR=%{_sysconfdir} \
    EMULATOR=SDLMAME
popd


%install
rm -rf $RPM_BUILD_ROOT

pushd sdlmess
QTDIR=%{_prefix} make install DESTDIR=$RPM_BUILD_ROOT DISTCFG=1 \
    PRETTY=0 CTIME=0 PREFIX=%{_prefix} SYSCONFDIR=%{_sysconfdir} \
    EMULATOR=SDLMESS QT_TRANSLATION=../../qt4/translations
popd

#remove the qmc2.ini since we only need one
rm -f $RPM_BUILD_ROOT%{_sysconfdir}/qmc2/qmc2.ini

pushd sdlmame
QTDIR=%{_prefix} make install DESTDIR=$RPM_BUILD_ROOT DISTCFG=1 \
    PRETTY=0 CTIME=0 PREFIX=%{_prefix} SYSCONFDIR=%{_sysconfdir} \
    EMULATOR=SDLMAME QT_TRANSLATION=../../qt4/translations
popd

# remove docs since we are intalling docs in %doc
pushd $RPM_BUILD_ROOT%{_datadir}/%{name}
rm -fr doc
ln -s ../doc/%{name}-%{version} doc
popd

#validate the desktop files
desktop-file-validate $RPM_BUILD_ROOT%{_datadir}/applications/qmc2-sdlmame.desktop
desktop-file-validate $RPM_BUILD_ROOT%{_datadir}/applications/qmc2-sdlmess.desktop

#fix the executable permissions
chmod 755 $RPM_BUILD_ROOT%{_bindir}/qmc2-sdlmame
chmod 755 $RPM_BUILD_ROOT%{_bindir}/qmc2-sdlmess
chmod 755 $RPM_BUILD_ROOT%{_bindir}/runonce


%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr(-,root,root,-)
%doc sdlmame/data/doc/html
%config(noreplace) %{_sysconfdir}/qmc2
%{_bindir}/runonce
%{_datadir}/qmc2


%files sdlmame
%defattr(-,root,root,-)
%{_bindir}/qmc2
%{_bindir}/qmc2-sdlmame
%{_datadir}/applications/qmc2-sdlmame.desktop


%files sdlmess
%defattr(-,root,root,-)
%{_bindir}/qmc2-sdlmess
%{_datadir}/applications/qmc2-sdlmess.desktop


%changelog
* Mon Jul 20 2009 Julian Sikorski <belegdol[at]gmail[dot]com> - 0.2-0.14.b10
- Updated to 0.2b10

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
