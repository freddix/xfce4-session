%define		xfce_version	4.10.0

Summary:	Xfce session manager
Name:		xfce4-session
Version:	4.10.0
Release:	1
License:	GPL v2
Group:		X11/Applications
Source0:	http://archive.xfce.org/src/xfce/xfce4-session/4.10/%{name}-%{version}.tar.bz2
# Source0-md5:	4768e1a41a0287af6aad18b329a0f230
Patch0:		499a719019e03da90b6901bb0f8a89d06ae167ee.patch
Patch1:		54002463867cdd01d5639e6a44f3bc74cd50f9ff.patch
Patch2:		7a75a8a0f7089b716e702e6bb0cf13fc3194e3db.patch
Patch3:		9f3077be682355e1cd07e9a9463e76307292208c.patch
Patch4:		%{name}-systemd.patch
URL:		http://www.xfce.org/
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	dbus-glib-devel
BuildRequires:	gettext-devel
BuildRequires:	intltool
BuildRequires:	libtool
BuildRequires:	libwnck2-devel
BuildRequires:	libxfce4ui-devel >= %{xfce_version}
BuildRequires:	pkg-config
BuildRequires:	xfce4-dev-tools >= %{xfce_version}
BuildRequires:	xfconf-devel >= %{xfce_version}
Requires(post,postun):	/usr/bin/gtk-update-icon-cache
Requires(post,postun):	hicolor-icon-theme
Requires:	%{name}-libs = %{version}-%{release}
Requires:	dbus-launch
Requires:	systemd
Requires:	xfconf
Requires:	xorg-app-iceauth
Suggests:	xscreensaver
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
xfce4-session is the session manager for the Xfce desktop environment.

%package libs
Summary:	Xfce Session Manager library
Group:		Libraries

%description libs
Xfce Session Manager library.

%package devel
Summary:	Header files for Xfce Session Manager library
Group:		Development/Libraries
Requires:	%{name}-libs = %{version}-%{release}

%description devel
Header files for Xfce Session Manager library.

%prep
%setup -q
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1

%build
%{__intltoolize}
%{__libtoolize}
%{__aclocal}
%{__autoheader}
%{__automake}
%{__autoconf}
%configure \
	ICEAUTH=/usr/bin/iceauth 	\
	--disable-silent-rules		\
	--disable-static		\
	--enable-systemd
%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT	\
	docdir="%{_datadir}/xfce4/help/%{name}"

rm -rf $RPM_BUILD_ROOT%{_datadir}/locale/ur_PK
rm -f $RPM_BUILD_ROOT%{_libdir}/xfce4/*/*/*.la

%find_lang %{name}

%clean
rm -rf $RPM_BUILD_ROOT

%post
%update_icon_cache hicolor

%postun
%update_icon_cache hicolor

%post	libs -p /usr/sbin/ldconfig
%postun	libs -p /usr/sbin/ldconfig

%files -f %{name}.lang
%defattr(644,root,root,755)
%doc AUTHORS COPYING ChangeLog NEWS README TODO
%attr(755,root,root) %{_bindir}/startxfce4
%attr(755,root,root) %{_bindir}/xfce4-session
%attr(755,root,root) %{_bindir}/xfce4-session-logout
%attr(755,root,root) %{_bindir}/xfce4-session-settings
%attr(755,root,root) %{_bindir}/xflock4

%dir %{_libdir}/xfce4/session
%dir %{_libdir}/xfce4/session/splash-engines
%attr(755,root,root) %{_libdir}/xfce4/session/balou-*
%attr(755,root,root) %{_libdir}/xfce4/session/xfsm-shutdown-helper
%attr(755,root,root) %{_libdir}/xfce4/session/splash-engines/*.so

%{_sysconfdir}/xdg/xfce4/xfconf/xfce-perchannel-xml/xfce4-session.xml
%attr(755,root,root) %{_sysconfdir}/xdg/xfce4/xinitrc
%attr(755,root,root) %{_sysconfdir}/xdg/xfce4/Xft.xrdb
%{_sysconfdir}/xdg/autostart/xscreensaver.desktop

%{_datadir}/xsessions/xfce.desktop
%{_datadir}/themes/Default/balou
%{_desktopdir}/*.desktop
%{_iconsdir}/hicolor/*/*/*.png
%{_iconsdir}/hicolor/*/*/*.svg
%{_mandir}/man1/*.1*

%files libs
%defattr(644,root,root,755)
%attr(755,root,root) %ghost %{_libdir}/libxfsm-*.so.?
%attr(755,root,root) %{_libdir}/libxfsm-*.so.*.*.*

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libxfsm-*.so
%{_includedir}/xfce4/xfce4-session-*
%{_pkgconfigdir}/xfce4-session-*.pc

