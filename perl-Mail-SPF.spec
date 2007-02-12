#
# Conditional build:
%bcond_without	autodeps	# don't BR packages needed only for resolving deps
%bcond_without	tests		# do not perform "make test"
#
%include	/usr/lib/rpm/macros.perl
%define		pdir	Mail
%define		pnam	SPF
Summary:	Mail::SPF - Mail Sender Authentication
Summary(pl.UTF-8):	Mail::SPF - uwierzytelnianie wysyłającego pocztę
Name:		perl-Mail-SPF
Version:	2.00
Release:	0.1
# "same as perl"
License:	GPL or Artistic
Group:		Development/Languages/Perl
Source0:	http://www.cpan.org/modules/by-module/%{pdir}/%{pdir}-%{pnam}-%{version}.tar.gz
# Source0-md5:	7fb935f9f070d5df092dc46f34975b00
URL:		http://search.cpan.org/dist/Mail-SPF/
BuildRequires:	perl-devel >= 1:5.8.0
BuildRequires:	rpm-perlprov >= 4.1-13
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
%setup -q -n %{pdir}-%{pnam}-%{version}

%build
%{__perl} Makefile.PL \
	INSTALLDIRS=vendor

%{__make}

%{?with_tests:%{__make} test}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} pure_install \
	DESTDIR=$RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_examplesdir}/%{name}-%{version}
install eg/dns.pl $RPM_BUILD_ROOT%{_examplesdir}/%{name}-%{version}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%{perl_vendorlib}/Mail/SPF.pm
%dir %{perl_vendorlib}/Mail/SPF
%{perl_vendorlib}/Mail/SPF/*.pm
%dir %{perl_vendorlib}/Mail/SPF/Mech
%{perl_vendorlib}/Mail/SPF/Mech/*.pm
%{_mandir}/man3/*
%dir %{_examplesdir}/%{name}-%{version}
%{_examplesdir}/%{name}-%{version}/dns.pl
