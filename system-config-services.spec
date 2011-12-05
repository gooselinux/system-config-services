%{!?python_sitelib: %global python_sitelib %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib(0)")}
%{!?python_version: %global python_version %(%{__python} -c "from distutils.sysconfig import get_python_version; print get_python_version()")}

%if 0%{?fedora}%{?rhel} == 0 || 0%{?fedora} >= 12 || 0%{?rhel} >= 6
%bcond_without polkit1
%endif

# Enterprise versions pull in docs automatically
%if 0%{?rhel} > 0
%bcond_without require_docs
%else
%bcond_with require_docs
%endif

Summary: Utility to start and stop system services
Name: system-config-services
Version: 0.99.45
Release: 1%{?dist}.3
URL: http://fedorahosted.org/%{name}
Source0: http://fedorahosted.org/released/%{name}/%{name}-%{version}.tar.bz2
Patch0: system-config-services-0.99.45-translations.patch.bz2
License: GPLv2+
Group: Applications/System
BuildArch: noarch
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires: python
BuildRequires: python-devel
BuildRequires: gettext
BuildRequires: intltool
BuildRequires: sed
BuildRequires: desktop-file-utils
Requires: chkconfig
Requires: gamin-python
Requires: hicolor-icon-theme
Requires: initscripts
Requires: pygtk2
Requires: pygtk2-libglade
Requires: python >= 2.3.0
Requires: dbus-python
Requires: python-slip >= 0.1.11
Requires: python-slip-dbus >= 0.2.8
Requires: python-slip-gtk
# Until version 0.99.28, system-config-services contained online documentation.
# From version 0.99.29 on, online documentation is split off into its own
# package system-config-services-docs. The following ensures that updating from
# earlier versions gives you both the main package and documentation.
Obsoletes: system-config-services < 0.99.29
%if %{with require_docs}
Requires: system-config-services-docs
%endif

%description
system-config-services is a utility which allows you to configure which
services should be enabled on your machine.

%prep
%setup -q
%patch0 -p1 -b .translations

%build
make %{?_smp_mflags}

%install
rm -rf %{buildroot}
make DESTDIR=%buildroot \
%if %{with polkit1}
    POLKIT0_SUPPORTED=0 \
%else
    POLKIT1_SUPPORTED=0 \
%endif
    install

desktop-file-install --vendor system --delete-original      \
  --dir %{buildroot}%{_datadir}/applications                \
  --add-category X-Red-Hat-Base                             \
  %{buildroot}%{_datadir}/applications/%{name}.desktop

%find_lang %name

%post
touch --no-create %{_datadir}/icons/hicolor
if [ -x %{_bindir}/gtk-update-icon-cache ]; then
  %{_bindir}/gtk-update-icon-cache --quiet %{_datadir}/icons/hicolor || :
fi

%postun
touch --no-create %{_datadir}/icons/hicolor
if [ -x %{_bindir}/gtk-update-icon-cache ]; then
  %{_bindir}/gtk-update-icon-cache --quiet %{_datadir}/icons/hicolor || :
fi

%clean
rm -rf %{buildroot}

%files -f %{name}.lang
%defattr(-,root,root,-)
%doc COPYING
%{_sbindir}/*
%{_bindir}/*
%{_datadir}/applications/system-config-services.desktop
%{_datadir}/icons/hicolor/48x48/apps/system-config-services.png
%{_datadir}/system-config-services
%{python_sitelib}/scservices
%{python_sitelib}/scservices-%{version}-py%{python_version}.egg-info
%{python_sitelib}/scservices.dbus-%{version}-py%{python_version}.egg-info

%{_sysconfdir}/dbus-1/system.d/org.fedoraproject.Config.Services.conf
%{_datadir}/dbus-1/system-services/org.fedoraproject.Config.Services.service
%if %{with polkit1}
%{_datadir}/polkit-1/actions/org.fedoraproject.config.services.policy
%else
%{_datadir}/PolicyKit/policy/org.fedoraproject.config.services.policy
%endif

%{_mandir}/*/system-config-services.8*

%changelog
* Fri Aug 06 2010 Nils Philippsen <nils@redhat.com> - 0.99.45-1.3
- just copy po files from git to work around "msgfmt -C ..." weirdness
  (#575677)

* Fri Aug 06 2010 Nils Philippsen <nils@redhat.com> - 0.99.45-1.2
- pick up translation updates (#575677)

* Wed Jun 30 2010 Nils Philippsen <nils@redhat.com> - 0.99.45-1.1
- require docs in enterprise builds

* Tue Jun 22 2010 Nils Philippsen <nils@redhat.com> - 0.99.45-1
- pick up translation updates

* Mon Apr 12 2010 Nils Philippsen <nils@redhat.com>
- remove obsolete PolicyKit-authentication-agent dependency (#581084)

* Tue Mar 23 2010 Nils Philippsen <nils@redhat.com> - 0.99.44-1
- pick up translation updates

* Thu Mar 11 2010 Nils Philippsen <nils@redhat.com> - 0.99.43-1
- use improved @polkit.enable_proxy decorator to gracefully catch some
  authorization failures (#543599)

* Mon Mar 08 2010 Nils Philippsen <nils@redhat.com> - 0.99.42-1
- add is_chkconfig_running() to dbus chkconfig service API (#539672)
- fix undefined names

* Thu Feb 25 2010 Nils Philippsen <nils@redhat.com>
- remove script hash-bangs from ordinary modules

* Tue Sep 29 2009 Nils Philippsen <nils@redhat.com> - 0.99.41-1
- initialize subscribers at the right place
- pick up new translations

* Thu Sep 24 2009 Nils Philippsen <nils@redhat.com>
- require python-slip-dbus >= 0.2.5

* Mon Sep 14 2009 Nils Philippsen <nils@redhat.com> - 0.99.40-1
- pick up updated translations

* Wed Sep 02 2009 Nils Philippsen <nils@redhat.com> - 0.99.39-1
- initialize gettext correctly

* Wed Aug 26 2009 Nils Philippsen <nils@redhat.com>
- explain obsoleting old versions (#519300)

* Tue Aug 25 2009 Nils Philippsen <nils@redhat.com> - 0.99.38-1
- always allow access if properly authorized

* Tue Aug 25 2009 Nils Philippsen <nils@redhat.com> - 0.99.37-1
- differentiate dbus interfaces in derived classes

* Tue Aug 25 2009 Nils Philippsen <nils@redhat.com> - 0.99.36-1
- support PolicyKit 1.0 (#500007)

* Tue Aug 11 2009 Nils Philippsen <nils@redhat.com> - 0.99.35-1
- use "chkconfig --type ..." if available (#467871)

* Tue Aug 11 2009 Nils Philippsen <nils@redhat.com> - 0.99.34-1
- avoid unnecessary recursions (#504964)
- fix DeprecationWarning in dbus mechanism

* Wed Jun 10 2009 Nils Philippsen <nils@redhat.com>
- improve xinetd service description text (#441258)

* Thu May 28 2009 Nils Philippsen <nils@redhat.com>
- use simplified source URL

* Tue Apr 14 2009 Nils Philippsen <nils@redhat.com> - 0.99.33-1
- pick up updated translations

* Mon Mar 01 2009 Nils Philippsen <nils@redhat.com> - 0.99.32-1
- require PolicyKit-authentication-agent from F-11 on (#487200)

* Thu Feb 19 2009 Nils Philippsen <nils@redhat.com> - 0.99.31-1
- don't traceback on chkconfig errors (#467871)

* Mon Dec 22 2008 Nils Philippsen <nils@redhat.com> - 0.99.30-1
- fix typo in Source0 URL

* Tue Dec 09 2008 Nils Philippsen <nils@redhat.com>
- allow anyone to invoke dbus methods (#475203)

* Fri Nov 28 2008 Nils Philippsen <nils@redhat.com> - 0.99.29-1
- split off documentation
- remove obsolete build requirement perl(XML::Parser)

* Mon Nov 24 2008 Nils Philippsen <nils@redhat.com>
- improve summary

* Thu Nov 20 2008 Nils Philippsen <nils@redhat.com> - 0.99.28-1
- improve fixing runlevels hookable set updates
- pick up updated translations

* Thu Nov 13 2008 Nils Philippsen <nils@redhat.com> - 0.99.27-1
- fix runlevels hookable set updates (custom runlevels dialog)

* Wed Nov 12 2008 Nils Philippsen <nils@redhat.com>
- use different defaults for PolicyKit authorizations (#470329)

* Mon Nov 10 2008 Nils Philippsen <nils@redhat.com> - 0.99.26-1
- make XinetdService._set_enabled() work for the first time
- fix GUI upon disabled services (#470722)

* Tue Oct 28 2008 Nils Philippsen <nils@redhat.com> - 0.99.25-1
- let gettext return the correct encoding (#468351)
- backout use of slip.dbus.proxy.unknown_method_default as this breaks things
  drastically

* Fri Oct 17 2008 Nils Philippsen <nils@redhat.com>
- use slip.dbus.proxy.unknown_method_default to handle objects that vanished
  from the bus

* Wed Oct 15 2008 Nils Philippsen <nphilipp@redhat.com> - 0.99.24-1
- use slip.dbus.polkit.AreAuthorizationsObtainable() to determine whether to
  use the dbus backend or not (#461688)
- pull in updated translations

* Fri Oct 10 2008 Nils Philippsen <nphilipp@redhat.com>
- default to not using dbus as root and using dbus otherwise (#461688)

* Mon Oct 06 2008 Nils Philippsen <nphilipp@redhat.com>
- revert erroneous po-file commit

* Wed Sep 24 2008 Nils Philippsen <nphilipp@redhat.com>
- get rid of POTFILES.in (#463592)

* Wed Sep 17 2008 Nils Philippsen <nphilipp@redhat.com>
- set whole hpaned (in)sensitive, not individual child widgets
- display busy cursor until all services are listed

* Mon Sep 15 2008 Nils Philippsen <nphilipp@redhat.com>
- make details notebook (in)sensitive along with services list
- remove debug print

* Fri Sep 12 2008 Nils Philippsen <nphilipp@redhat.com> - 0.99.23-1
- make double-thaws of notications fail
- ensure correct order replay of frozen notifications when thawing (#460598)
- ensure list is sensitive when dealing with herders that are ready already
  (e.g. in the case of already running backend)
- avoid premature herder ready signals
- XinetdServiceHerder: delay added/deleted services signals only after startup

* Tue Aug 26 2008 Nils Philippsen <nphilipp@redhat.com> - 0.99.22-1
- version 0.99.22

* Tue Aug 26 2008 Nils Philippsen <nphilipp@redhat.com>
- make services list insensitive until first batch of services has rolled in

* Fri Aug 22 2008 Nils Philippsen <nphilipp@redhat.com>
- honor X-Fedora-Pidfile directive in LSB header
- implement default priorities for AsyncCmdQueue objects
- service gtk events in GUIServicesList.on_services_changed () to avoid hanging
  GUI on startup

* Thu Aug 21 2008 Nils Philippsen <nphilipp@redhat.com>
- let GUI wait until herders are ready, then select first service in list
- remove debugging output
- when the selected service is deleted, find a suitable alternative to select
- change PolicyKit actions to org.fedoraproject.config.services.info,
  org.fedoraproject.config.services.manage
- when listing services, don't sleep until backend herder is ready
- handle SVC_HERDER_READY signal with empty service name

* Wed Aug 20 2008 Nils Philippsen <nphilipp@redhat.com>
- make monitoring of initially stopped services with pidfiles work

* Mon Aug 18 2008 Nils Philippsen <nphilipp@redhat.com>
- use %%global for %%python_sitelib, %%python_version

* Fri Aug 15 2008 Nils Philippsen <nphilipp@redhat.com>
- remove some cruft
- DBUS objects get a bus name, not the bus itself when created

* Tue Aug 12 2008 Nils Philippsen <nphilipp@redhat.com>
- rectify dbus interface name

* Fri Aug 08 2008 Nils Philippsen <nphilipp@redhat.com>
- use HookableSet for DBusSysVServiceProxy.runlevels
- set about dialog transient for main window

* Wed Aug 06 2008 Nils Philippsen <nphilipp@redhat.com>
- don't except KeyboardInterrupt in two places

* Tue Aug 05 2008 Nils Philippsen <nphilipp@redhat.com> - 0.99.21-1
- get rid of save() methods, save instantly on changes instead

* Thu Jul 24 2008 Nils Philippsen <nphilipp@redhat.com> - 0.99.20-1
- use new slip.dbus API as of python-slip-0.1.7

* Wed Jul 23 2008 Nils Philippsen <nphilipp@redhat.com> - 0.99.19-1
- use new slip.dbus API as of python-slip-0.1.6

* Wed Jul 23 2008 Nils Philippsen <nphilipp@redhat.com> - 0.99.18-1
- require PolicyKit-gnome instead of usermode

* Tue Jul 22 2008 Nils Philippsen <nphilipp@redhat.com> - 0.99.17-1
- remove pam/consolehelper cruft

* Mon Jul 21 2008 Nils Philippsen <nphilipp@redhat.com> - 0.99.16-1
- add dbus and PolicyKit integration

* Fri Apr 04 2008 Nils Philippsen <nphilipp@redhat.com> - 0.99.15-1
- pick up updated translations
- remove unnecessary *.orig files

* Fri Apr 04 2008 Nils Philippsen <nphilipp@redhat.com> - 0.99.14-1
- indent runlevel checkboxes in "Customize Runlevels" dialog
- set rules hint for services treeview
- tweak services detail widgets

* Fri Apr 04 2008 Nils Philippsen <nphilipp@redhat.com> - 0.99.13-1
- distribute gtk_label_autowrap.py (#440582)

* Fri Apr 04 2008 Nils Philippsen <nphilipp@redhat.com> - 0.99.12-1
- make manpage syntactically and semantically correct (#221200, patch by Eric
  Raymond) and update it

* Wed Apr 02 2008 Nils Philippsen <nphilipp@redhat.com> - 0.99.11-1
- make service description labels wrap automatically, avoid gratuitous resizing
  of service list (#440197)

* Tue Mar 25 2008 Nils Philippsen <nphilipp@redhat.com> - 0.99.10-1
- use hard links to avoid excessive disk space requirements

* Thu Mar 13 2008 Nils Philippsen <nphilipp@redhat.com> - 0.99.9-1
- fix traceback when setting GUI elements (in)sensitive (#437289)
- fix generating localized XML files
- update online docs po/pot files only on real changes

* Fri Mar 07 2008 Nils Philippsen <nphilipp@redhat.com> - 0.99.8-1
- don't warn about xinetd not installed/running with disabled xinetd services
  in the list

* Thu Mar 06 2008 Nils Philippsen <nphilipp@redhat.com> - 0.99.7-1
- update online documentation
- reload xinetd on changing xinetd services
- honor xinetd status when displaying xinetd services

* Tue Mar 04 2008 Nils Philippsen <nphilipp@redhat.com> - 0.99.6-1
- use ListStore instead of TreeStore
- add some extra padding for fixed width columns in TreeView

* Tue Mar 04 2008 Nils Philippsen <nphilipp@redhat.com> - 0.99.5-1
- implement custom runlevel menu

* Mon Mar 03 2008 Nils Philippsen <nphilipp@redhat.com> - 0.99.4-1
- use gettext directly instead of rhpl
- add popup menu for enabling SysV services in specific runlevels
- display help
- enable custom runlevels via customization dialog

* Fri Feb 29 2008 Nils Philippsen <nphilipp@redhat.com> - 0.99.3-1
- add gamin-python requirement (#435068)
- monitor /proc/<pid> for services with known pidfile(s)

* Wed Feb 27 2008 Nils Philippsen <nphilipp@redhat.com> - 0.99.2-1
- import missing os.path (#435068)

* Wed Feb 27 2008 Nils Philippsen <nphilipp@redhat.com> - 0.99.1-1
- make gui.py executable (#435068)

* Fri Feb 22 2008 Nils Philippsen <nphilipp@redhat.com> - 0.99.0-1
- make start/stop/restart/enable/disable buttons/menu entries work
- SysVService: SVC_ENABLED_YES <-> RL 2, 3, 4, 5; everything else is
  SVC_ENABLED_CUSTOM

* Thu Feb 21 2008 Nils Philippsen <nphilipp@redhat.com>
- implement XinetdServiceInfo.parse()
- add and implement SVC_STATUS_REFRESHING
- clear description text buffers if not description exists
- implement GUIXinetdServicesDetailsPainter.paint_details()
- implement async loading in XinetdService
- implement GUISysVServiceEntryPainter.paint()
- handle deleted services in GUIServicesList.on_service_status_changed()
- make menu items and toolbar buttons (in)sensitive based on selected service

* Wed Feb 20 2008 Nils Philippsen <nphilipp@redhat.com>
- add classes dealing with information about services, e.g. contained in
  chkconfig/LSB style comments in init scripts
- distinguish real SysV services from fake ones (e.g. halt)
- set enabled/disabled icons for SysV services
- add textual description about if a service is enabled/disabled/customized
- display description, short description

* Sun Feb 17 2008 Nils Philippsen <nphilipp@redhat.com>
- use lower default priority for asynchronous IO handling
- remove more obsolete files
- symlink gui.py instead of obsolete serviceconf.py to system-config-services
- write status and explanation labels
- make some labels selectable
- use default geometry of 800x400
- use stock warning icon for dead services

* Sat Feb 16 2008 Nils Philippsen <nphilipp@redhat.com>
- move handling of service changes from GUIServicesTreeStore into
  GUIServicesList
- use stock icons for enabled/status columns
- use event loop instead of threads for asynchronously running external commands

* Fri Feb 15 2008 Nils Philippsen <nphilipp@redhat.com>
- implement status updates

* Thu Feb 14 2008 Nils Philippsen <nphilipp@redhat.com>
- move getstatusoutput() into util.py
- watch runlevels 0 and 6 as well
- notify subscribers on service changes
- ignore non-chkconfig-capable "services" in /etc/init.d, /etc/rc?.d
- add infrastructure for asynchronous loading/saving of services

* Wed Feb 13 2008 Nils Philippsen <nphilipp@redhat.com>
- new GUI, backend implementation

* Wed Jan 30 2008 Nils Philippsen <nphilipp@redhat.com> - 0.9.20-1
- migrate online help to yelp/Docbook XML

* Fri Jan 11 2008 Nils Philippsen <nphilipp@redhat.com> - 0.9.19-1
- use config-util for userhelper configuration from Fedora 9 on (#428407)

* Thu Dec 27 2007 Nils Philippsen <nphilipp@redhat.com> - 0.9.18-1
- rename sr@Latn to sr@latin (#426590)

* Wed Dec 05 2007 Nils Philippsen <nphilipp@redhat.com>
- overwrite *.pot and *.po files only on real changes

* Mon Oct 15 2007 Nils Philippsen <nphilipp@redhat.com> - 0.9.17-1
- avoid traceback when neither xdg-open nor htmlview is found

* Mon Oct 15 2007 Nils Philippsen <nphilipp@redhat.com> - 0.9.16-1
- add release tag to remaining changelog versions to appease rpmlint
- don't let gtk-update-icon-cache fail scriptlets
- re-add plain hicolor-icon-theme requirement to avoid unowned directories
- remove obsolete no.po translation file (#332411)

* Mon Oct 15 2007 Nils Philippsen <nphilipp@redhat.com> - 0.9.15-1
- Merge review (#226470):
  - remove hicolor-icon-theme, gtk2 requirements, call gtk-update-icon-cache
    with full path

* Mon Oct 15 2007 Nils Philippsen <nphilipp@redhat.com> - 0.9.14-1
- Merge review (#226470):
  - remove shebang line from nonblockingreader.py

* Mon Oct 15 2007 Nils Philippsen <nphilipp@redhat.com> - 0.9.13-1
- Merge review (#226470):
  - make obsoletes versioned
  - escape RPM macro in changelog
  - change license tag to GPLv2+
  - recoded documentation to UTF-8
  - install files with correct permissions
  - add release to changelog versions to appease rpmlint
  - use %%config(noreplace)
  - use "make %%{?_smp_mflags}"
  - use "%%defattr(-,root,root,-)"
  - use xdg-open if available
- pick up updated translations

* Mon Oct 08 2007 Nils Philippsen <nphilipp@redhat.com> - 0.9.12-1
- add "make diff" ("dif") and "make shortdiff" ("sdif")
- pull in updated translations

* Tue Oct 02 2007 Nils Philippsen <nphilipp@redhat.com> - 0.9.11-1
- pick up updated translations

* Mon Sep 10 2007 Nils Philippsen <nphilipp@redhat.com>
- make use of force tagging (since mercurial 0.9.4)

* Mon Jul 23 2007 Nils Philippsen <nphilipp@redhat.com> - 0.9.10-1
- make "make archive" work with Hg
- disable automatic ChangeLog generation

* Wed Jun 27 2007 Nils Philippsen <nphilipp@redhat.com> - 0.9.9-1
- fix desktop file category (#245891)

* Fri May 04 2007 Nils Philippsen <nphilipp@redhat.com> - 0.9.8-1
- pick up updated translations (#223447)

* Wed Apr 25 2007 Nils Philippsen <nphilipp@redhat.com> - 0.9.7-1
- pick up updated translations
- work around issues with UTF-8 in translatable strings (#232809)

* Thu Mar 22 2007 Nils Philippsen <nphilipp@redhat.com>
- update URL

* Tue Mar 20 2007 Nils Philippsen <nphilipp@redhat.com>
- mention that we are upstream
- use preferred buildroot
- fix licensing blurb in PO files
- recode spec file to UTF-8

* Wed Jan 31 2007 Nils Philippsen <nphilipp@redhat.com> - 0.9.6-1
- fix up service metadata reading a bit (#217591)

* Wed Jan 31 2007 Nils Philippsen <nphilipp@redhat.com> - 0.9.5-1
- use "install -m" to install a lot of files without executable bits (#222579)

* Wed Dec  6 2006 Harald Hoyer <harald@redhat.com> - 0.9.4-1
- fixed service start/stop (#218429)
- translation update (#216558)
- Resolves: rhbz#216558, rhbz#218429

* Fri Nov 24 2006 Nils Philippsen <nphilipp@redhat.com> - 0.9.3-1
- pick up updated translations (#216558)

* Fri Oct 20 2006 Nils Philippsen <nphilipp@redhat.com> - 0.9.2-1
- use intltool-extract for i18n of glade files (#211248) and desktop file
  (#207345)

* Tue Sep 05 2006 Nils Philippsen <nphilipp@redhat.com> - 0.9.1-1
- don't disable Start/Stop/Restart upon reverting changes (#202722)
- add dist tag
- install po files (again)
- require gettext for building
- fix tagging for make archive
- fix circular make dependency
- remove duplicate message definitions

* Fri Aug 18 2006 Nils Philippsen <nphilipp@redhat.com>
- make revert work again (#202467)
- don't show all runlevels when starting

* Mon Jun 05 2006 Jesse Keating <jkeating@redhat.com> - 0.9.0-2
- Added BuildRequires perl-XML-Parser (#194179)
- Added Requires(post) and (postun) gtk2

* Fri May 19 2006 Nils Philippsen <nphilipp@redhat.com>
- rip out autofoo
- use bzip2'ed tarballs

* Fri Mar 03 2006 Nils Philippsen <nphilipp@redhat.com> - 0.9.0-1
- require hicolor-icon-theme (#182878, #182879)

* Wed Feb 28 2006 Florian Festi <ffesti@redhat.com> 
- rewrote large parts of servicemethods (OO design, better handling of old/new
  settings, read headers of init scripts completely)
- first implementation of widgets to control services (intended for tools
  configuring single services like nfs, samba, bind, ...), still missing: i18n,
  dependencies on other services (like portmap)

* Fri Jan 27 2006 Nils Philippsen <nphilipp@redhat.com> - 0.8.99.2-1
- fix saving xinetd services

* Fri Jan 27 2006 Nils Philippsen <nphilipp@redhat.com> - 0.8.99.1-1
- implement daemons and xinetd services on separate tabs

* Mon Jan 09 2006 Nils Philippsen <nphilipp@redhat.com>
- separate daemons and xinetd based services
- enable Serbian translation files

* Fri Oct 14 2005 Nils Philippsen <nphilipp@redhat.com>
- don't use pam_stack (#170645)

* Tue Aug 16 2005 Nils Philippsen <nphilipp@redhat.com> - 0.8.26-1
- revamp getting output from external commands (#162884)
- package %%{_bindir}/serviceconf symlink (#165099)

* Mon May 09 2005 Nils Philippsen <nphilipp@redhat.com> - 0.8.25-1
- pick up updated translations

* Fri May 06 2005 Nils Philippsen <nphilipp@redhat.com> - 0.8.24-1
- make "make update-po" pick up translatable strings in desktop file (#156801)

* Fri May 06 2005 Nils Philippsen <nphilipp@redhat.com> - 0.8.23-1
- pick up new translations

* Wed Apr 27 2005 Jeremy Katz <katzj@redhat.com> - 0.8.22-2
- silence %%post

* Fri Apr 01 2005 Nils Philippsen <nphilipp@redhat.com> 0.8.22-1
- fix deprecation warnings (#153052) with patch by Colin Charles
- update the GTK+ theme icon cache on (un)install (Christopher Aillon)

* Thu Mar 24 2005 Nils Philippsen <nphilipp@redhat.com> 0.8.21-1
- connect toggled signals of service/runlevel checkboxes to enable saving again
  (#151982)
- consolidate on_optRL*_toggled
- connect delete_event of mainWindow to ask whether things should be saved
  before quitting
- tab -> space indentation to avoid ambiguity
- change some typos

* Fri Mar 18 2005 Nils Philippsen <nphilipp@redhat.com> 0.8.20-1
- don't read from /dev/null when restarting xinetd/services to prevent hangs
- build toolbar in glade to avoid DeprecationWarnings (#134978)
- dynamic, translated column titles for runlevel columns

* Thu Feb 17 2005 Daniel J Walsh <dwalsh@redhat.com> 0.8.19-1
- Added patch from Charlie Brej 

* Fri Jan 28 2005 Nils Philippsen <nphilipp@redhat.com> 0.8.18-1
- fix off-by-one which prevented saving changes to the last service in the list
  (#139456)

* Tue Jan 04 2005 Nils Philippsen <nphilipp@redhat.com> 0.8.17-1
- throw away stderr to not be confused by error messages (#142983)

* Wed Dec 08 2004 Nils Philippsen <nphilipp@redhat.com> 0.8.16-1
- don't hardcode python 2.3 (#142246)
- remove some cruft from configure.in

* Wed Oct 20 2004 Nils Philippsen <nphilipp@redhat.com> 0.8.15-1
- include all languages (#136460)

* Tue Oct 12 2004 Nils Philippsen <nphilipp@redhat.com> 0.8.14-1
- actually install nonblockingreader module (#135445)

* Mon Oct 11 2004 Nils Philippsen <nphilipp@redhat.com> 0.8.12-1
- really update UI when reading from pipes (#120579, #135215)

* Fri Oct 08 2004 Nils Philippsen <nphilipp@redhat.com> 0.8.11-1
- fix gtk.main*() related DeprecationWarnings (#134978)

* Fri Oct 01 2004 Daniel J Walsh <dwalsh@redhat.com> 0.8.10-1
- Update translations

* Mon Sep 27 2004 Nils Philippsen <nphilipp@redhat.com> - 0.8.9-1
- enable Arabic translation (#133722)

* Thu Sep 23 2004 Nils Philippsen <nphilipp@redhat.com> - 0.8.8.1-1
- get in updated translations (#133137)
- appease make distcheck
- pick up updated autofoo scripts

* Wed Jun 16 2004 Brent Fox <bfox@redhat.com> - 0.8.8-9
- use watch cursor when starting and stopping services (bug #122425)

* Mon Apr 12 2004 Brent Fox <bfox@redhat.com> 0.8.8-8
- fix icon path (bug #120184)

* Tue Apr  6 2004 Brent Fox <bfox@redhat.com> 0.8.8-7
- remove extra strip (bug #119624)

* Mon Apr  5 2004 Brent Fox <bfox@redhat.com> 0.8.8-6
- code around new verbosity in libglade (bug #119622)

* Wed Mar 31 2004 Brent Fox <bfox@redhat.com> 0.8.8-5
- fix typo (bug #119559)

* Wed Mar 24 2004 Brent Fox <bfox@redhat.com> 0.8.8-4
- increase default size of the main window

* Fri Mar 19 2004 Brent Fox <bfox@redhat.com> 0.8.8-3
- make app exit properly on window close (bug #118762)

* Wed Mar 17 2004 Brent Fox <bfox@redhat.com> 0.8.8-2
- bump release

* Tue Mar 16 2004 Brent Fox <bfox@redhat.com> 0.8.8-1
- work around problem with libglade

* Wed Mar  3 2004 Brent Fox <bfox@redhat.com> 0.8.7-2
- add a BuildRequires on automake17

* Tue Mar  2 2004 Brent Fox <bfox@redhat.com> 0.8.7-1
- remove dependency on gnome-python2 and gnome-python2-canvas
- try to load glade file in the cwd, if not, pull from /usr/share/
- apply patch from bug #117277

* Tue Jan 6 2004 Daniel J Walsh <dwalsh@redhat.com> 0.8.6-3
- Fix console app so it launches properly

* Tue Jan 6 2004 Daniel J Walsh <dwalsh@redhat.com> 0.8.6-2
- remove requirement for 2.2

* Thu Nov 11 2003 Daniel J Walsh <dwalsh@redhat.com> 0.8.6-1
- Rename system-config-services

* Wed Oct 17 2003 Daniel J Walsh <dwalsh@redhat.com> 0.8.5-23
- Add all translated languages

* Fri Oct 17 2003 Daniel J Walsh <dwalsh@redhat.com> 0.8.5-22
- Remove /dev/null from status

* Mon Oct 6 2003 Daniel J Walsh <dwalsh@redhat.com> 0.8.5-21
- Fix crash on about

* Wed Oct 1 2003 Daniel J Walsh <dwalsh@redhat.com> 0.8.5-20
- bump

* Wed Oct 1 2003 Daniel J Walsh <dwalsh@redhat.com> 0.8.5-19
- Fix pathing problem on Hammer

* Fri Sep 5 2003 Daniel J Walsh <dwalsh@redhat.com> 0.8.5-18
- bump

* Fri Sep 5 2003 Daniel J Walsh <dwalsh@redhat.com> 0.8.5-17
- bump
* Fri Sep 5 2003 Daniel J Walsh <dwalsh@redhat.com> 0.8.5-16
- Eliminate debugging message

* Mon Aug 25 2003 Daniel J Walsh <dwalsh@redhat.com> 0.8.5-15
-  For some reason this did not make it to RHN Trying again. By Bumping version.

* Tue Aug 5 2003 Daniel J Walsh <dwalsh@redhat.com> 0.8.5-14
- Bumped version for rhl

* Tue Aug 5 2003 Daniel J Walsh <dwalsh@redhat.com> 0.8.5-13
- Remove depracated call

* Wed Jul 30 2003 Daniel J Walsh <dwalsh@redhat.com> 0.8.5-12
- Bumped version for rhl

* Wed Jul 30 2003 Daniel J Walsh <dwalsh@redhat.com> 0.8.5-11
- Changed handling of xinetd services to show xinetd service status

* Wed Jul 30 2003 Daniel J Walsh <dwalsh@redhat.com> 0.8.5-10
- Bumped version for rhl

* Tue Jul 29 2003 Daniel J Walsh <dwalsh@redhat.com> 0.8.5-9
- Allow services to have ':'s in them.

* Wed Jul 9 2003 Daniel J Walsh <dwalsh@redhat.com> 0.8.5-8
- Bumped version for rhl

* Wed Jul 9 2003 Daniel J Walsh <dwalsh@redhat.com> 0.8.5-7
- Add ability to add and delete services

* Tue Jun 17 2003 Daniel J Walsh <dwalsh@redhat.com> 0.8.5-6
- Bumped version for rhel

* Thu Jun 5 2003 Daniel J Walsh <dwalsh@redhat.com> 0.8.5-5
- Minor fixes to match GUI users guide and fix icon

* Tue May  27 2003 Daniel J Walsh <dwalsh@redhat.com> 0.8.5-4
- Bumped version for rhel

* Tue May  27 2003 Daniel J Walsh <dwalsh@redhat.com> 0.8.5-3
- Moved system-config-service.png to /usr/share/system-config-services

* Fri Mar  7 2003 Daniel J Walsh <dwalsh@redhat.com> 0.8.5-2
- Bumped version for rhel

* Tue Mar  4 2003 Daniel J Walsh <dwalsh@redhat.com> 0.8.5-1
- Fix swiching runlevels on modified screens.

* Tue Feb  25 2003 Daniel J Walsh <dwalsh@redhat.com> 0.8.4-2
- Fix dissapearing text on selecting toggle.

* Tue Jan  28 2003 Daniel J Walsh <dwalsh@redhat.com> 0.8.4-1
- Release Candidate
- Fix Icon

* Tue Jan  28 2003 Daniel J Walsh <dwalsh@redhat.com> 0.8.3-12
- Fix Language Problems

* Tue Jan  28 2003 Daniel J Walsh <dwalsh@redhat.com> 0.8.3-11
- Fix handling of errors in /etc/init.d directory

* Tue Jan  14 2003 Daniel J Walsh <dwalsh@redhat.com> 0.8.3-10
- Update documentation

* Thu Jan  9 2003 Daniel J Walsh <dwalsh@redhat.com> 0.8.3-9
- Added StartupNotify=true
- Added accellerators

* Thu Dec  12 2002 Daniel J Walsh <dwalsh@redhat.com> 0.8.3-8
- Update help docs

* Fri Dec  6 2002 Daniel J Walsh <dwalsh@redhat.com> 0.8.3-7
- Fix error catching on invalid display

* Tue Dec  3 2002 Daniel J Walsh <dwalsh@redhat.com> 0.8.3-6
- Fix DISPLAY error handling
- Stretch Screen size
- Update status box after Start/Stop/Restart
- Fix Icon error

* Thu Nov 14 2002 Dan Walsh <dwalsh@redhat.com> 0.8.3-5
- Fix reading of descriptions from startup scripts to ignore blank lines

* Thu Nov 14 2002 Dan Walsh <dwalsh@redhat.com> 0.8.3-4
- Add scrollbar to description and status

* Thu Oct 24 2002 Dan Walsh <dwalsh@redhat.com> 0.8.3-3
- Fix internal handling of version number.

* Thu Oct 10 2002 Dan Walsh <dwalsh@redhat.com> 0.8.3-2
- Remove buttons from screen to match GNOME standards

* Tue Oct 1 2002 Dan Walsh <dwalsh@redhat.com> 0.8.3-1
- Change GUI Presentation and add service status

* Wed Sep 4 2002 Bill Nottingham <notting@redhat.com> 0.8.2-1
- fix startup in some locales

* Tue Sep 3 2002 Dan Walsh <dwalsh@redhat.com> 0.8.1-13
- Update translations

* Tue Aug 27 2002 Dan Walsh <dwalsh@redhat.com> 0.8.1-12
- Update translations
- Fix multi-processor problem with popen

* Tue Aug 20 2002 Dan Walsh <dwalsh@redhat.com> 0.8.1-11
- Use gnome url_show for help
- fix legal notice

* Mon Aug 19 2002 Dan Walsh <dwalsh@redhat.com> 0.8.1-10
- Fix word wrap
- Fix initial startup to select first row
- Update languages

* Sat Aug 10 2002 Dan Walsh <dwalsh@redhat.com> 0.8.1-9
- eliminate extra python files not intended for release

* Wed Aug 7 2002 Dan Walsh <dwalsh@redhat.com> 0.8.1-8
- Update dependencies

* Mon Aug 5 2002 Dan Walsh <dwalsh@redhat.com> 0.8.1-7
- Updated internationalization stuff

* Wed Jul 31 2002 Dan Walsh <dwalsh@redhat.com> 0.8.1-6
- Updated internationalization stuff

* Fri Jul 26 2002 Dan Walsh <dwalsh@redhat.com> 0.8.1-5
- Updated to use intltool and new build environment.
- Added with pam changes for timestamp
- New internationalization stuff

* Tue Jul 23 2002 Dan Walsh <dwalsh@redhat.com>
- Fix the desktop file, using new naming standards.
- Fix the error outpur

* Mon Jul 22 2002 Dan Walsh <dwalsh@redhat.com>
- Fix clock cursor, set app insensitive until services loaded"

* Mon Jul 22 2002 Tammy Fox <tfox@redhat.com>
- Updated docs

* Wed Jul  17 2002 Dan Walsh <dwalsh@redhat.com> 0.8.1-1
- Fix internationalization problems.  Clean up glade port.

* Thu Jul  11 2002 Dan Walsh <dwalsh@redhat.com> 0.8.1-1
- complete rename to system-config-services

* Tue Jul  9 2002 Dan Walsh <dwalsh@redhat.com> 0.8.1-1
- complete gtk2 port, Fix Help, About, fix minor bugs

* Wed May 29 2002 Bill Nottingham <notting@redhat.com> 0.8.0-1
- initial hack gtk2 port

* Mon Apr 15 2002 Trond Eivind Glomsrød <teg@redhat.com> 0.7.0-3
- Update translations

* Wed Apr 10 2002 Bill Nottingham <notting@redhat.com> 0.7.0-2
- fix docs (#63179)

* Tue Apr  9 2002 Bill Nottingham <notting@redhat.com>
- add some more cases to #60384 fix

* Sun Apr  7 2002 Jeremy Katz <katzj@redhat.com>
- don't show rpmsave, rpmnew, rpmorig, or .swp files (#60384)

* Tue Apr  2 2002 Nalin Dahyabhai <nalin@redhat.com>
- set up userhelper for system-config-services

* Fri Jan 25 2002 Bill Nottingham <notting@redhat.com>
- add patch to fix startup when there are services with 'hide' set

* Fri Aug 24 2001 Tim Powers <timp@redhat.com>
- fixed typo in Requires /;sbin/chkconfig

* Fri Aug 24 2001 Bill Nottingham <notting@redhat.com>
- build with new translations
- move system-config-services link to /usr/bin

* Fri Aug 17 2001 Bill Nottingham <notting@redhat.com>
- translation typos (#51774, #51776)
- add system-config-services link
- if we're using find_lang, don't specify the .mo files explicitly

* Mon Aug 13 2001 Tim Powers <timp@redhat.com>
- updated serviceconf.gladestrings

* Fri Aug 10 2001 Tim Powers <timp@redhat.com>
- languified specfile for additional translations

* Thu Aug  9 2001 Alexander Larsson <alexl@redhat.com> 0.6.1-1
- Add an icon

* Thu Aug  9 2001 Alexander Larsson <alexl@redhat.com>
- Install in sysconfig.

* Tue Aug  7 2001 Tim Powers <timp@redhat.com>
- gnomified
- work around parsing languified chkconfig output so that we can get accurate information displayed

* Tue Jul 31 2001 Tim Powers <timp@redhat.com>
- languified since we now serve multiple languages

* Mon Jul 30 2001 Yukihiro Nakai <ynakai@redhat.com>
- User %%fine_lang
- Add Japanese translation.

* Mon Jul 30 2001 Preston Brown <pbrown@redhat.com>
- clean up title display
- make sure initial highlighted entry also displays description info

* Wed Jul 18 2001 Tammy Fox <tfox@redhat.com>
- added help doc
- moved man page into man directory
- added Makefile for man page
- added man page to spec file

* Mon Jul  9 2001 Tim Powers <timp@redhat.com>
- languify to shutup rpmlint

* Thu Jul  5 2001 Tim Powers <timp@redhat.com>
- removed TODO and README, added COPYING file to docs

* Tue May 15 2001 Tim Powers <timp@redhat.com>
- Initial build.


