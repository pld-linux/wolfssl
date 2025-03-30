#
# Conditional build:
%bcond_without	apidocs		# API documentation
%bcond_without	static_libs	# static library
#
Summary:	wolfSSL - small, fast, portable implementation of TLS/SSL for embedded devices to the cloud
Summary(pl.UTF-8):	wolfSSL - mała, szybka, przenośna implementacja TLS/SSL dla urządzeń wbudowanych
Name:		wolfssl
Version:	5.7.2
Release:	1
License:	GPL v2 or commercial
Group:		Libraries
#Source0Download: https://github.com/wolfSSL/wolfssl/releases
Source0:	https://github.com/wolfSSL/wolfssl/archive/v%{version}-stable/%{name}-%{version}-stable.tar.gz
# Source0-md5:	bc28818fb83b793b6c23987e1b116735
Patch0:		%{name}-x32.patch
URL:		https://www.wolfssl.com/
BuildRequires:	autoconf >= 2.69
BuildRequires:	automake >= 1:1.14.1
%{?with_apidocs:BuildRequires:	doxygen}
BuildRequires:	libtool >= 2:2.4.2
BuildRequires:	rpm-build >= 4.6
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
The wolfSSL embedded SSL library (formerly CyaSSL) is a lightweight
SSL/TLS library written in ANSI C and targeted for embedded, RTOS, and
resource-constrained environments - primarily because of its small
size, speed, and feature set. wolfSSL supports industry standards up
to the current TLS 1.3 and DTLS 1.2 and offers progressive ciphers
such as ChaCha20, Curve25519, Blake2b and Post-Quantum TLS 1.3 groups.

%description -l pl.UTF-8
Wbudowana biblioteka SSL wolfSSL (dawniej CyaSSL) to lekka biblioteka
SSL/TLS napisana w ANSI C i przeznaczona przede wszystkim do środowisk
wbudowanych, czasu rzeczywistego i o ograniczonych zasobach - głównie
ze względu na mały rozmiar, szybkość i funkcjonalność. wolfSSL
obsługuje standardy przemysłowe do aktualnego TLS 1.3 oraz DTLS 1.2 i
oferuje progresywne szyfry, takie jak ChaCha20, Curve25519, Blake2b
czy grupy Post-Quantum TLS 1.3.

%package devel
Summary:	Header files for wolfSSL library
Summary(pl.UTF-8):	Pliki nagłówkowe biblioteki wolfSSL
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}

%description devel
Header files for wolfSSL library.

%description devel -l pl.UTF-8
Pliki nagłówkowe biblioteki wolfSSL.

%package static
Summary:	Static wolfSSL library
Summary(pl.UTF-8):	Statyczna biblioteka wolfSSL
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
Static wolfSSL library.

%description static -l pl.UTF-8
Statyczna biblioteka wolfSSL.

%package apidocs
Summary:	API documentation for wolfSSL library
Summary(pl.UTF-8):	Dokumentacja API biblioteki wolfSSL
Group:		Documentation
BuildArch:	noarch

%description apidocs
API documentation for wolfSSL library.

%description apidocs -l pl.UTF-8
Dokumentacja API biblioteki wolfSSL.

%prep
%setup -q -n %{name}-%{version}-stable
%patch -P0 -p1

%build
%{__libtoolize}
%{__aclocal} -I m4
%{__autoconf}
%{__autoheader}
%{__automake}
%configure \
	--enable-all \
	--enable-quic \
	--disable-silent-rules \
	%{?with_static_libs:--enable-static}
%{__make}

%if %{with apidocs}
cd doc
./generate_documentation.sh -html
%endif

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

# obsoleted by pkg-config
%{__rm} $RPM_BUILD_ROOT%{_libdir}/libwolfssl.la
# packaged as %doc
%{__rm} -r $RPM_BUILD_ROOT%{_docdir}/wolfssl

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc ChangeLog.md LICENSING README.md doc/{QUIC.md,README.txt}
%attr(755,root,root) %{_libdir}/libwolfssl.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libwolfssl.so.42

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/wolfssl-config
%attr(755,root,root) %{_libdir}/libwolfssl.so
%{_includedir}/wolfssl
%{_pkgconfigdir}/wolfssl.pc

%if %{with static_libs}
%files static
%defattr(644,root,root,755)
%{_libdir}/libwolfssl.a
%endif

%if %{with apidocs}
%files apidocs
%defattr(644,root,root,755)
%doc doc/html/*
%endif
