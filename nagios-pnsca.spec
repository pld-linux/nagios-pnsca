#
# Conditional build:
%bcond_without	tests		# build without tests

Summary:	Persistent NSCA feeder
Name:		nagios-pnsca
Version:	0.1
Release:	0.1
License:	GPL v2
Group:		Applications
Source0:	http://git.op5.org/git/?p=nagios/pnsca.git;a=snapshot;h=7738b4d59fde56afb68cc78b0f43333ee808157a;sf=tgz#/pnsca.tgz
# Source0-md5:	4afe19942467f966282a4e6e90987032
URL:		http://git.op5.org/git/?p=nagios/pnsca.git
Requires:	nagios
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		brokerdir	%{_libdir}/nagios/brokers

%description
This module does the equivalent of running the OCSP and OCHP commands,
but with a persistent connection to the command we're supposed to run,
continuously feeding it host and service check results on stdin in the
format used by send_nsca.

%prep
%setup -qc
mv pnsca-*/* .

%build
%{__make} V=1 \
	CC="%{__cc}" \
	OPTFLAGS="%{rpmcflags} -fPIC" \
	LDFLAGS="%{rpmldflags}"

%if %{with tests}
ln -sf pnsca.so posh.so
%{__make} test
%endif

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{brokerdir}
install -p pnsca.so $RPM_BUILD_ROOT%{brokerdir}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%attr(755,root,root) %{brokerdir}/pnsca.so
