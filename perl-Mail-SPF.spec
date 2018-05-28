#
# Conditional build:
%bcond_without	tests		# do not perform "make test"
#
%include	/usr/lib/rpm/macros.perl
%define		pdir	Mail
%define		pnam	SPF
Summary:	Mail::SPF - Mail Sender Authentication
Summary(pl.UTF-8):	Mail::SPF - uwierzytelnianie wysyłającego pocztę
Name:		perl-Mail-SPF
Version:	2.9.0
Release:	1
# "same as perl"
License:	GPL or Artistic
Group:		Development/Languages/Perl
Source0:	http://www.cpan.org/modules/by-module/%{pdir}/%{pdir}-%{pnam}-v%{version}.tar.gz
# Source0-md5:	664e20d79c87fa505080f362e827dace
Patch0:		tests-fix.patch
URL:		http://search.cpan.org/dist/Mail-SPF/
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
%setup -q -n %{pdir}-%{pnam}-v%{version}
%patch0 -p1

%build
%{__perl} Makefile.PL \
	INSTALLDIRS=vendor

%{__make}

%{?with_tests:%{__make} test}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} pure_install \
	DESTDIR=$RPM_BUILD_ROOT

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
