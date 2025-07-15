#
# Conditional build:
%bcond_without	tests		# do not perform "make test"
#
%define		pdir	Mail
%define		pnam	SPF
Summary:	Mail::SPF - Mail Sender Authentication
Summary(pl.UTF-8):	Mail::SPF - uwierzytelnianie wysyłającego pocztę
Name:		perl-Mail-SPF
Version:	3.20240206
Release:	1
# "same as perl"
License:	GPL or Artistic
Group:		Development/Languages/Perl
Source0:	http://www.cpan.org/modules/by-module/%{pdir}/%{pdir}-%{pnam}-%{version}.tar.gz
# Source0-md5:	da1b4b35241de31553bc00626db90c12
Patch0:		tests-fix.patch
URL:		http://search.cpan.org/dist/Mail-SPF/
BuildRequires:	perl-Module-Build
BuildRequires:	perl-devel >= 1:5.8.0
BuildRequires:	rpm-perlprov >= 4.1-13
%if %{with tests}
BuildRequires:	perl-Net-DNS >= 0.58
BuildRequires:	perl-NetAddr-IP
BuildRequires:	perl-version
BuildRequires:	perl-Net-DNS-Resolver-Programmable
%endif
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_noautoreq_perl		Mail::SPF::GlobalMod

%description
This is an initial draft object oriented reimplementation of
Mail::SPF::Query. It is not yet fully tested, and does not yet contain
all of the additional features expected of a practical SPF
implementation.

%description -l pl.UTF-8
To jest początkowa zorientowana obiektowo reimplementacja
Mail::SPF::Query. Nie jest jeszcze w pełni przetestowana i nie zawiera
jeszcze wszystkich dodatkowych możliwości oczekiwanych od praktycznej
implementacji SPF.

%prep
%setup -q -n %{pdir}-%{pnam}-%{version}
%patch -P0 -p1

# These tests mess around with resolv.conf and networking
# that are not present on builders
%{__rm} t/00.04-class-server.t t/00.05-class-macrostring.t


%build
%{__perl} Makefile.PL \
	INSTALLDIRS=vendor

%{__make}

%{?with_tests:%{__make} test}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} pure_install \
	DESTDIR=$RPM_BUILD_ROOT

# Move spfd from /usr/bin to /usr/sbin to keep path same
# as in older versions, note: needs spfd-path.patch!
install -d $RPM_BUILD_ROOT%{_sbindir}
%{__mv} $RPM_BUILD_ROOT%{_bindir}/spfd $RPM_BUILD_ROOT%{_sbindir}/

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/spfquery
%attr(755,root,root) %{_sbindir}/spfd
%{perl_vendorlib}/Mail/SPF.pm
%dir %{perl_vendorlib}/Mail/SPF
%{perl_vendorlib}/Mail/SPF/*.pm
%dir %{perl_vendorlib}/Mail/SPF/Mech
%{perl_vendorlib}/Mail/SPF/Mech/*.pm
%{perl_vendorlib}/Mail/SPF/Mod
%{perl_vendorlib}/Mail/SPF/v1
%{perl_vendorlib}/Mail/SPF/v2
%{_mandir}/man1/*
%{_mandir}/man3/*
