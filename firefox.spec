# TODO:
# - consider --enable-libproxy
#
# Conditional build:
%bcond_with	tests		# enable tests (whatever they check)
%bcond_without	gtk3		# GTK+ 3.x instead of 2.x
%bcond_without	kerberos	# disable krb5 support
%bcond_without	official	# official Firefox branding
%bcond_without	pgo		# PGO-enabled build (requires working $DISPLAY == :100)
# - disabled shared_js - https://bugzilla.mozilla.org/show_bug.cgi?id=1039964
%bcond_with	shared_js	# shared libmozjs library [broken]

# On updating version, grab CVE links from:
# https://www.mozilla.org/security/known-vulnerabilities/firefox.html
# Release Notes:
# https://developer.mozilla.org/en-US/Firefox/Releases

# The actual sqlite version (see RHBZ#480989):
%define		sqlite_build_version %(pkg-config --silence-errors --modversion sqlite3 2>/dev/null || echo ERROR)

%define		nspr_ver	4.12
%define		nss_ver		3.26.2

Summary:	Firefox web browser
Summary(hu.UTF-8):	Firefox web böngésző
Summary(pl.UTF-8):	Firefox - przeglądarka WWW
Name:		firefox
Version:	50.1.0
Release:	2
License:	MPL v2.0
Group:		X11/Applications/Networking
Source0:	http://releases.mozilla.org/pub/mozilla.org/firefox/releases/%{version}/source/firefox-%{version}.source.tar.xz
# Source0-md5:	0f6a56cd8da8fa9deedfd61bcb43a65d
Source3:	%{name}.desktop
Source4:	%{name}.sh
Source5:	vendor.js
Source6:	vendor-ac.js
Patch0:		idl-parser.patch
Patch1:		xulrunner-new-libxul.patch
Patch2:		xulrunner-paths.patch
Patch3:		xulrunner-pc.patch
Patch4:		%{name}-prefs.patch
Patch5:		%{name}-pld-bookmarks.patch
Patch6:		%{name}-no-subshell.patch
Patch7:		%{name}-middle_click_paste.patch
Patch8:		%{name}-system-virtualenv.patch
Patch9:		%{name}-Disable-Firefox-Health-Report.patch
Patch10:	freetype.patch
Patch11:	%{name}-nss-http2.patch
URL:		https://www.mozilla.org/firefox/
BuildRequires:	OpenGL-devel
BuildRequires:	alsa-lib-devel
BuildRequires:	automake
BuildRequires:	autoconf2_13
BuildRequires:	bzip2-devel
BuildRequires:	cairo-devel >= 1.10.2-5
BuildRequires:	dbus-glib-devel >= 0.60
BuildRequires:	fontconfig-devel >= 1:2.7.0
BuildRequires:	freetype-devel >= 1:2.1.8
BuildRequires:	gcc-c++ >= 6:4.4
BuildRequires:	glib2-devel >= 1:2.22
BuildRequires:	gstreamer-devel >= 1.0
BuildRequires:	gstreamer-plugins-base-devel >= 1.0
%{!?with_gtk3:BuildRequires:	gtk+2-devel >= 2:2.18.0}
%{?with_gtk3:BuildRequires:	gtk+3-devel >= 3.4.0}
%{?with_kerberos:BuildRequires:	heimdal-devel >= 0.7.1}
BuildRequires:	hunspell-devel >= 1.2.3
BuildRequires:	libIDL-devel >= 0.8.0
# DECnet (dnprogs.spec), not dummy net (libdnet.spec)
#BuildRequires:	libdnet-devel
BuildRequires:	libevent-devel >= 1.4.7
# standalone libffi 3.0.9 or gcc's from 4.5(?)+
BuildRequires:	libffi-devel >= 6:3.0.9
BuildRequires:	libicu-devel >= 50.1
# requires libjpeg-turbo implementing at least libjpeg 6b API
BuildRequires:	libjpeg-devel >= 6b
BuildRequires:	libjpeg-turbo-devel
BuildRequires:	libpng(APNG)-devel >= 0.10
BuildRequires:	libpng-devel >= 2:1.6.23
BuildRequires:	libstdc++-devel >= 6:4.4
BuildRequires:	libvpx-devel >= 1.5.0
BuildRequires:	nspr-devel >= 1:%{nspr_ver}
BuildRequires:	nss-devel >= 1:%{nss_ver}
BuildRequires:	pango-devel >= 1:1.22.0
BuildRequires:	pixman-devel >= 0.19.2
BuildRequires:	perl-modules >= 5.004
BuildRequires:	pkgconfig
BuildRequires:	pkgconfig(libffi) >= 3.0.9
BuildRequires:	pulseaudio-devel
BuildRequires:	python-modules >= 1:2.5
%{?with_pgo:BuildRequires:	python-modules-sqlite}
BuildRequires:	python-simplejson
BuildRequires:	python-virtualenv >= 15
BuildRequires:	readline-devel
BuildRequires:	rpm >= 4.4.9-56
BuildRequires:	rpmbuild(macros) >= 1.601
BuildRequires:	sed >= 4.0
BuildRequires:	sqlite3-devel >= 3.13.0
BuildRequires:	startup-notification-devel >= 0.8
BuildRequires:	xorg-lib-libX11-devel
BuildRequires:	xorg-lib-libXScrnSaver-devel
BuildRequires:	xorg-lib-libXcomposite-devel
BuildRequires:	xorg-lib-libXdamage-devel
BuildRequires:	xorg-lib-libXext-devel
BuildRequires:	xorg-lib-libXfixes-devel
BuildRequires:	xorg-lib-libXinerama-devel
BuildRequires:	xorg-lib-libXt-devel
%{?with_pgo:BuildRequires:	xorg-xserver-Xvfb}
%ifarch %{x8664}
BuildRequires:	yasm >= 1.0.1
%endif
BuildRequires:	zip
BuildRequires:	zlib-devel >= 1.2.3
BuildConflicts:	%{name}-devel < %{version}
Requires(post):	mktemp >= 1.5-18
Requires:	browser-plugins >= 2.0
Requires:	desktop-file-utils
Requires:	hicolor-icon-theme
Requires:	myspell-common
Requires:	nspr >= 1:%{nspr_ver}
Requires:	nss >= 1:%{nss_ver}
Requires:	%{name}-libs = %{version}-%{release}
Provides:	wwwbrowser
Obsoletes:	iceweasel
Obsoletes:	mozilla-firebird
Obsoletes:	mozilla-firefox
Obsoletes:	mozilla-firefox-lang-en < 2.0.0.8-3
Obsoletes:	mozilla-firefox-libs
Obsoletes:	xulrunner
Obsoletes:	xulrunner-gnome
Conflicts:	firefox-lang-resources < %{version}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		filterout_cpp		-D_FORTIFY_SOURCE=[0-9]+

# don't satisfy other packages
%define		_noautoprovfiles	%{_libdir}/%{name}

# and as we don't provide them, don't require either
%define		_noautoreq	libmozjs.so libxul.so

%description
Firefox is an open-source web browser, designed for standards
compliance, performance and portability.

%description -l hu.UTF-8
Firefox egy nyílt forrású webböngésző, hatékonyságra és
hordozhatóságra tervezve.

%description -l pl.UTF-8
Firefox jest przeglądarką WWW rozpowszechnianą zgodnie z ideami
ruchu otwartego oprogramowania oraz tworzoną z myślą o zgodności ze
standardami, wydajnością i przenośnością.

%package libs
Summary:	Firefox shared libraries
Summary(pl.UTF-8):	Biblioteki współdzielone Firefoxa
Group:		X11/Libraries
Requires:	cairo >= 1.10.2-5
Requires:	dbus-glib >= 0.60
Requires:	fontconfig-libs >= 1:2.7.0
Requires:	glib2 >= 1:2.22
%{!?with_gtk3:Requires:	gtk+2 >= 2:2.18.0}
%{?with_gtk3:Requires:	gtk+3 >= 3.4.0}
Requires:	libjpeg-turbo
Requires:	libpng >= 2:1.6.23
Requires:	libpng(APNG) >= 0.10
Requires:	libvpx >= 1.5.0
Requires:	pango >= 1:1.22.0
Requires:	sqlite3 >= %{sqlite_build_version}
Requires:	startup-notification >= 0.8
Provides:	xulrunner-libs = 2:%{version}-%{release}
Obsoletes:	iceweasel-libs
Obsoletes:	xulrunner-libs

%description libs
XULRunner shared libraries.

%description libs -l pl.UTF-8
Biblioteki współdzielone XULRunnera.

%package devel
Summary:	Headers for developing programs that will use Firefox
Summary(pl.UTF-8):	Pliki nagłówkowe do tworzenia programów używających Firefox
Group:		X11/Development/Libraries
Requires:	%{name}-libs = %{version}-%{release}
Requires:	nspr-devel >= 1:%{nspr_ver}
Requires:	nss-devel >= 1:%{nss_ver}
Requires:	python-ply
Provides:	xulrunner-devel = 2:%{version}-%{release}
Obsoletes:	iceweasel-devel
Obsoletes:	mozilla-devel
Obsoletes:	mozilla-firefox-devel
Obsoletes:	seamonkey-devel
Obsoletes:	xulrunner-devel

%description devel
Firefox development package.

%description devel -l pl.UTF-8
Pakiet programistyczny Firefoxa.

%prep
%setup -q

# avoid using included headers (-I. is before HUNSPELL_CFLAGS)
%{__rm} extensions/spellcheck/hunspell/src/{*.hxx,hunspell.h}
# hunspell needed for factory including mozHunspell.h
echo 'LOCAL_INCLUDES += $(MOZ_HUNSPELL_CFLAGS)' >> extensions/spellcheck/src/Makefile.in

%patch0 -p2
%patch1 -p1
%patch2 -p2
%patch3 -p1
%patch4 -p1
%patch5 -p1
%patch6 -p2
%patch7 -p1
%patch8 -p2
%patch9 -p1
%patch10 -p2
%patch11 -p1

%{__sed} -i -e '1s,/usr/bin/env python,%{__python},' xpcom/typelib/xpt/tools/xpt.py xpcom/idl-parser/xpidl/xpidl.py

%if %{with pgo}
%{__sed} -i -e 's@__BROWSER_PATH__@"../../dist/bin/firefox-bin"@' build/automation.py.in
%endif

%build
cp -p %{_datadir}/automake/config.* build/autoconf

cat << 'EOF' > .mozconfig
. $topsrcdir/browser/config/mozconfig

mk_add_options MOZ_OBJDIR=@TOPSRCDIR@/obj-%{_target_cpu}

# Options for 'configure' (same as command-line options).
ac_add_options --host=%{_target_platform}
ac_add_options --prefix=%{_prefix}
%if %{?debug:1}0
ac_add_options --disable-optimize
ac_add_options --enable-debug
ac_add_options --enable-debug-modules
ac_add_options --enable-debugger-info-modules
ac_add_options --enable-crash-on-assert
%else
ac_add_options --disable-debug
ac_add_options --enable-optimize="%{rpmcflags} -Os"
%endif
ac_add_options --disable-strip
ac_add_options --disable-install-strip
%if %{with tests}
ac_add_options --enable-tests
ac_add_options --enable-mochitest
%else
%if %{with pgo}
ac_add_options --enable-tests
%else
ac_add_options --disable-tests
%endif
%endif
ac_add_options --disable-crashreporter
ac_add_options --disable-gconf
ac_add_options --disable-gnomeui
ac_add_options --disable-necko-wifi
ac_add_options --disable-updater
ac_add_options --enable-chrome-format=omni
ac_add_options --enable-default-toolkit=%{?with_gtk3:cairo-gtk3}%{!?with_gtk3:cairo-gtk2}
ac_add_options --enable-extensions=default
ac_add_options --enable-gio
ac_add_options --enable-readline
ac_add_options --enable-safe-browsing
%{?with_shared_js:ac_add_options --enable-shared-js}
ac_add_options --enable-startup-notification
ac_add_options --enable-system-cairo
ac_add_options --enable-system-ffi
ac_add_options --enable-system-hunspell
ac_add_options --enable-system-sqlite
ac_add_options --enable-url-classifier
%{?with_official:ac_add_options --enable-official-branding}
ac_add_options --with-default-mozilla-five-home=%{_libdir}/%{name}
ac_add_options --with-distribution-id=org.pld-linux
ac_add_options --with-pthreads
ac_add_options --with-system-bz2
ac_add_options --with-system-icu
ac_add_options --with-system-jpeg
ac_add_options --with-system-libevent
ac_add_options --with-system-libvpx
ac_add_options --with-system-nspr
ac_add_options --with-system-nss
ac_add_options --with-system-png
ac_add_options --with-system-zlib
ac_add_options --with-x
EOF

%if %{with pgo}
D=$(( RANDOM % (200 - 100 + 1 ) + 5 ))
/usr/bin/Xvfb :${D} &
XVFB_PID=$!
[ -n "$XVFB_PID" ] || exit 1
export DISPLAY=:${D}
%{__make} -j1 -f client.mk profiledbuild \
	AUTOCONF=/usr/bin/autoconf2_13 \
	DESTDIR=obj-%{_target_cpu}/dist \
	MOZ_MAKE_FLAGS="%{_smp_mflags}"
kill $XVFB_PID
%else
%{__make} -j1 -f client.mk build \
	AUTOCONF=/usr/bin/autoconf2_13 \
	MOZ_MAKE_FLAGS="%{_smp_mflags}"
%endif

%install
rm -rf $RPM_BUILD_ROOT
install -d \
	$RPM_BUILD_ROOT{%{_bindir},%{_sbindir},%{_libdir}} \
	$RPM_BUILD_ROOT%{_desktopdir} \
	$RPM_BUILD_ROOT%{_datadir}/%{name}/browser \
	$RPM_BUILD_ROOT%{_libdir}/%{name}/browser/plugins \
	$RPM_BUILD_ROOT%{_libdir}/%{name}-devel/sdk/{lib,bin} \
	$RPM_BUILD_ROOT%{_includedir}/%{name} \
	$RPM_BUILD_ROOT%{_datadir}/idl/%{name} \
	$RPM_BUILD_ROOT%{_pkgconfigdir}

%browser_plugins_add_browser %{name} -p %{_libdir}/%{name}/browser/plugins

cd obj-%{_target_cpu}
%{__make} -C browser/installer stage-package libxul.pc libxul-embedding.pc mozilla-js.pc mozilla-plugin.pc \
	DESTDIR=$RPM_BUILD_ROOT \
	installdir=%{_libdir}/%{name} \
	INSTALL_SDK=1 \
	PKG_SKIP_STRIP=1

cp -aL browser/installer/*.pc $RPM_BUILD_ROOT%{_pkgconfigdir}
cp -aL dist/firefox/* $RPM_BUILD_ROOT%{_libdir}/%{name}/
cp -aL dist/idl/* $RPM_BUILD_ROOT%{_datadir}/idl/%{name}
cp -aL dist/include/* $RPM_BUILD_ROOT%{_includedir}/%{name}
cp -aL dist/include/xpcom-config.h $RPM_BUILD_ROOT%{_libdir}/%{name}-devel
cp -aL dist/sdk/lib/* $RPM_BUILD_ROOT%{_libdir}/%{name}-devel/sdk/lib
cp -aL dist/sdk/bin/* $RPM_BUILD_ROOT%{_libdir}/%{name}-devel/sdk/bin
find $RPM_BUILD_ROOT%{_libdir}/%{name}-devel/sdk -name "*.pyc" | xargs rm -f

ln -s %{_libdir}/%{name} $RPM_BUILD_ROOT%{_libdir}/%{name}-devel/bin
ln -s %{_includedir}/%{name} $RPM_BUILD_ROOT%{_libdir}/%{name}-devel/include
ln -s %{_datadir}/idl/%{name} $RPM_BUILD_ROOT%{_libdir}/%{name}-devel/idl
ln -s %{_libdir}/%{name}-devel/sdk/lib $RPM_BUILD_ROOT%{_libdir}/%{name}-devel/lib

# replace copies with symlinks
%{?with_shared_js:ln -sf %{_libdir}/%{name}/libmozjs.so $RPM_BUILD_ROOT%{_libdir}/%{name}-devel/sdk/lib/libmozjs.so}
ln -sf %{_libdir}/%{name}/libxul.so $RPM_BUILD_ROOT%{_libdir}/%{name}-devel/sdk/lib/libxul.so
# temp fix for https://bugzilla.mozilla.org/show_bug.cgi?id=63955
chmod a+rx $RPM_BUILD_ROOT%{_libdir}/%{name}-devel/sdk/bin/xpt.py

# move arch independant ones to datadir
mv $RPM_BUILD_ROOT%{_libdir}/%{name}/browser/chrome $RPM_BUILD_ROOT%{_datadir}/%{name}/browser/chrome
mv $RPM_BUILD_ROOT%{_libdir}/%{name}/browser/extensions $RPM_BUILD_ROOT%{_datadir}/%{name}/browser/extensions
mv $RPM_BUILD_ROOT%{_libdir}/%{name}/browser/icons $RPM_BUILD_ROOT%{_datadir}/%{name}/browser/icons
mv $RPM_BUILD_ROOT%{_libdir}/%{name}/defaults $RPM_BUILD_ROOT%{_datadir}/%{name}/browser/defaults
mv $RPM_BUILD_ROOT%{_datadir}/%{name}/browser/defaults/{pref,preferences}

ln -s ../../../share/%{name}/browser/chrome $RPM_BUILD_ROOT%{_libdir}/%{name}/browser/chrome
ln -s ../../../share/%{name}/browser/defaults $RPM_BUILD_ROOT%{_libdir}/%{name}/browser/defaults
ln -s ../../../share/%{name}/browser/extensions $RPM_BUILD_ROOT%{_libdir}/%{name}/browser/extensions
ln -s ../../../share/%{name}/browser/icons $RPM_BUILD_ROOT%{_libdir}/%{name}/browser/icons

%{__rm} -r $RPM_BUILD_ROOT%{_libdir}/%{name}/dictionaries
ln -s %{_datadir}/myspell $RPM_BUILD_ROOT%{_libdir}/%{name}/dictionaries

sed 's,@LIBDIR@,%{_libdir},' %{SOURCE4} > $RPM_BUILD_ROOT%{_bindir}/firefox
chmod 755 $RPM_BUILD_ROOT%{_bindir}/firefox

# install icons and desktop file
for i in 16 32 48 %{?with_official:22 24 256}; do
	install -d $RPM_BUILD_ROOT%{_iconsdir}/hicolor/${i}x${i}/apps
	cp -a ../browser/branding/%{!?with_official:un}official/default${i}.png \
		$RPM_BUILD_ROOT%{_iconsdir}/hicolor/${i}x${i}/apps/firefox.png
done

cp -a %{SOURCE3} $RPM_BUILD_ROOT%{_desktopdir}/%{name}.desktop

# install our settings
%if "%{pld_release}" == "ac"
cp -a %{SOURCE6} $RPM_BUILD_ROOT%{_datadir}/%{name}/browser/defaults/preferences/vendor.js
%else
cp -a %{SOURCE5} $RPM_BUILD_ROOT%{_datadir}/%{name}/browser/defaults/preferences/vendor.js
%endif

# files created by firefox -register
touch $RPM_BUILD_ROOT%{_libdir}/%{name}/browser/components/compreg.dat
touch $RPM_BUILD_ROOT%{_libdir}/%{name}/browser/components/xpti.dat

cat << 'EOF' > $RPM_BUILD_ROOT%{_sbindir}/%{name}-chrome+xpcom-generate
#!/bin/sh
umask 022
rm -f %{_libdir}/%{name}/browser/components/{compreg,xpti}.dat

# it attempts to touch files in $HOME/.mozilla
# beware if you run this with sudo!!!
export HOME=$(mktemp -d)
# also TMPDIR could be pointing to sudo user's homedir
unset TMPDIR TMP || :

%{_libdir}/%{name}/firefox -register

rm -rf $HOME
EOF
chmod 755 $RPM_BUILD_ROOT%{_sbindir}/%{name}-chrome+xpcom-generate

%clean
rm -rf $RPM_BUILD_ROOT

%post
%{_sbindir}/%{name}-chrome+xpcom-generate
%update_browser_plugins
%update_icon_cache hicolor
%update_desktop_database

%postun
if [ "$1" = 0 ]; then
	%update_browser_plugins
	%update_icon_cache hicolor
fi

%files
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/%{name}
%attr(755,root,root) %{_sbindir}/%{name}-chrome+xpcom-generate

%{_desktopdir}/firefox.desktop
%{_iconsdir}/hicolor/*/apps/firefox.png

# browser plugins v2
%{_browserpluginsconfdir}/browsers.d/%{name}.*
%config(noreplace) %verify(not md5 mtime size) %{_browserpluginsconfdir}/blacklist.d/%{name}.*.blacklist

%dir %{_libdir}/%{name}/browser
%dir %{_libdir}/%{name}/browser/components
%dir %{_libdir}/%{name}/browser/plugins
%dir %{_libdir}/%{name}/browser/features

%dir %{_datadir}/%{name}
%dir %{_datadir}/%{name}/browser
%dir %{_datadir}/%{name}/browser/extensions
%{_datadir}/%{name}/browser/chrome
%{_datadir}/%{name}/browser/defaults
%{_datadir}/%{name}/browser/icons

# symlinks
%{_libdir}/%{name}/browser/extensions
%{_libdir}/%{name}/browser/chrome
%{_libdir}/%{name}/browser/icons
%{_libdir}/%{name}/browser/defaults

%attr(755,root,root) %{_libdir}/%{name}/firefox
%attr(755,root,root) %{_libdir}/%{name}/firefox-bin
%attr(755,root,root) %{_libdir}/%{name}/run-mozilla.sh
%{_libdir}/%{name}/application.ini
%{_libdir}/%{name}/browser/blocklist.xml
%{_libdir}/%{name}/browser/chrome.manifest
%{_libdir}/%{name}/browser/components/components.manifest
%attr(755,root,root) %{_libdir}/%{name}/browser/components/libbrowsercomps.so
# the signature of the default theme
%{_datadir}/%{name}/browser/extensions/{972ce4c6-7e08-4474-a285-3208198ce6fd}.xpi
%{_libdir}/%{name}/browser/omni.ja

%{_libdir}/%{name}/browser/features/aushelper@mozilla.org.xpi
%{_libdir}/%{name}/browser/features/e10srollout@mozilla.org.xpi
%{_libdir}/%{name}/browser/features/firefox@getpocket.com.xpi
%{_libdir}/%{name}/browser/features/webcompat@mozilla.org.xpi

# files created by firefox -register
%ghost %{_libdir}/%{name}/browser/components/compreg.dat
%ghost %{_libdir}/%{name}/browser/components/xpti.dat

%attr(755,root,root) %{_libdir}/%{name}/plugin-container
%{_libdir}/%{name}/dictionaries

%dir %{_libdir}/%{name}/fonts
%{_libdir}/%{name}/fonts/EmojiOneMozilla.ttf

%dir %{_libdir}/%{name}/gmp-clearkey
%dir %{_libdir}/%{name}/gmp-clearkey/0.1
%{_libdir}/%{name}/gmp-clearkey/0.1/clearkey.info
%attr(755,root,root) %{_libdir}/%{name}/gmp-clearkey/0.1/libclearkey.so

%files libs
%defattr(644,root,root,755)
%dir %{_libdir}/%{name}
%{_libdir}/%{name}/platform.ini
%{?with_shared_js:%attr(755,root,root) %{_libdir}/%{name}/libmozjs.so}
%attr(755,root,root) %{_libdir}/%{name}/liblgpllibs.so
%attr(755,root,root) %{_libdir}/%{name}/libxul.so
%attr(755,root,root) %{_libdir}/%{name}/libmozavcodec.so
%attr(755,root,root) %{_libdir}/%{name}/libmozavutil.so
%{_libdir}/%{name}/dependentlibs.list
%{_libdir}/%{name}/omni.ja
%if %{with gtk3}
%dir %{_libdir}/%{name}/gtk2
%attr(755,root,root) %{_libdir}/%{name}/gtk2/libmozgtk.so
%attr(755,root,root) %{_libdir}/%{name}/libmozgtk.so
%endif

%files devel
%defattr(644,root,root,755)
%{_includedir}/%{name}
%{_datadir}/idl/%{name}
%dir %{_libdir}/%{name}-devel
%{_libdir}/%{name}-devel/bin
%{_libdir}/%{name}-devel/idl
%{_libdir}/%{name}-devel/lib
%{_libdir}/%{name}-devel/include
%{_libdir}/%{name}-devel/*.h
%dir %{_libdir}/%{name}-devel/sdk
%{_libdir}/%{name}-devel/sdk/lib
%dir %{_libdir}/%{name}-devel/sdk/bin
%attr(755,root,root) %{_libdir}/%{name}-devel/sdk/bin/header.py
%attr(755,root,root) %{_libdir}/%{name}-devel/sdk/bin/run-mozilla.sh
%attr(755,root,root) %{_libdir}/%{name}-devel/sdk/bin/typelib.py
%attr(755,root,root) %{_libdir}/%{name}-devel/sdk/bin/xpcshell
%attr(755,root,root) %{_libdir}/%{name}-devel/sdk/bin/xpidl.py
%{_libdir}/%{name}-devel/sdk/bin/xpidllex.py
%{_libdir}/%{name}-devel/sdk/bin/xpidlyacc.py
%attr(755,root,root) %{_libdir}/%{name}-devel/sdk/bin/xpt.py
%{_libdir}/%{name}-devel/sdk/bin/ply

%{_pkgconfigdir}/libxul.pc
%{_pkgconfigdir}/libxul-embedding.pc
%{_pkgconfigdir}/mozilla-js.pc
%{_pkgconfigdir}/mozilla-plugin.pc
