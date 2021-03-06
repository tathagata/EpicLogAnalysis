# Base Macros which need to be set
%define packageprefix fortune-mod-fortunes
%define packagebase shlomif
%define archivebase fortunes-shlomif
%define version 0.18.59
%define fortunefilesprefix shlomif-
%define rel 1

# Derived Macros
%define archivewithver %{archivebase}-%{version}
%define archivefull %{archivewithver}.tar.gz

%define fortunedatadir %{_datadir}/games/fortunes

Name: %{packageprefix}-%{packagebase}
Version: %{version}
Release: %{rel}
License: Free to use but restricted
Group: Toys

Source: http://www.shlomifish.org/humour/fortunes/%{archivefull}
BuildArch: noarch
Buildroot: %{_tmppath}/%{name}-root
URL: http://www.shlomifish.org/humour/fortunes/
BuildRequires: fortune-mod
Requires: fortune-mod
Summary: Fortune Cookies Collection by Shlomi Fish

%description
This package contains several collections of fortune cookies by Shlomi Fish.
Namely, a collection of his own quotes, some of his favourites from various
sources; a collection of excerpts from the T.V. Show Friends; the Rules of
Open Source Programming, and a collection of reasons why there is no IGLU
cabal.


%prep
%setup -n %{archivewithver}
cat <<EOF > README
This is a group of fortune files collected by Shlomi Fish.
EOF

%build

myprefix="%{fortunefilesprefix}"
rm -f *.dat
for fn in `ls | grep -v "\\." | grep -v "[[:upper:]]"` ; do
    mv "$fn" "${myprefix}$fn" ;
    /usr/sbin/strfile "${myprefix}$fn" "${myprefix}$fn.dat" ;
done

%install

rm -rf "$RPM_BUILD_ROOT"
mkdir -p "$RPM_BUILD_ROOT"/%{fortunedatadir}
for dat in *.dat ; do \
    cp "${dat}" "`echo "$dat" | sed 's/\.dat$//'`" \
        "$RPM_BUILD_ROOT"/%{fortunedatadir} ; \
done

%files
%defattr(-,root,root)
%{fortunedatadir}/*
%doc README

%clean
rm -rf "$RPM_BUILD_ROOT"

%changelog
* Wed Oct 08 2008 Shlomi Fish <shlomif@iglu.org.il> 0.10.148-1
- Updated slightly.

* Sun Jul 21 2002 Shlomi Fish <shlomif@iglu.org.il> 0.2.4-7
- Applied Tzafrir's Suggestions:
- Created the macro %{fortunedatadir} to specify the locations of the files
- Broke up long lines.
- Added fortune-mod to the BuildRequires
- Made the script /bin/sh compatible
- Changed a mkdir loop to mkdir -p
- Removed the empty %post and %postun targets
- Added a README file.


* Fri May 31 2002 Shlomi Fish <shlomif@iglu.org.il> 0.2.2-2
- Added macros all over the place

* Thu May 30 2002 Shlomi Fish <shlomif@iglu.org.il> 0.2.2-1
- first release - testing.

