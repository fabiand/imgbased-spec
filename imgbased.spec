
%global commit 71b82f3c0f5720dd4eb372630d6e01a08bf32b7e
%global shortcommit %(c=%{commit}; echo ${c:0:7})
%global commitdate 20140721
%global gitversion .git%{commitdate}.%{shortcommit}
%global source https://github.com/fabiand/%{name}/archive/%{commit}/%{name}-%{version}%{gitversion}.tar.gz

Summary:        Tools to work with an image based rootfs
Name:           imgbased
Version:        0.1
Release:        0.8%{?gitversion}%{?dist}

License:        GPLv2+
URL:            https://github.com/fabiand/%{name}
Source0:        %{?source}
BuildArch:      noarch

BuildRequires:  autoconf
BuildRequires:  automake
BuildRequires:  python2-devel
BuildRequires:  asciidoc
BuildRequires:  pylint
BuildRequires:  pyflakes
BuildRequires:  python-pep8
%if 0%{?fedora} > 19
BuildRequires:  python-pexpect
%else
BuildRequires:  pexpect
%endif

Requires:       lvm2


%description
imgbased provides a specific management method to derive writable file-system
layers from read-only base images. It also takes care that the layer which
shall be used can be selected at boot time.

In a nutshell this works by:

 * having a boot partition
 * and having a default LVM volume group (HostVG)
 * which has a thinpool
 * each base is kept in a read-only thin logical volume in the thinpool
 * for each base at least one writable layer, which is a thin logical volume, is
   created in the thinpool
 * for each layer a boot entry is created which can be used to boot in a
   specific layer


%package kickstarts
Summary:        Kickstarts to create some related images
Group:          Applications/System
BuildRequires:  pykickstart
Requires:       lorax


%description kickstarts
This is a collection of kickstarts to create images to test
the tool.
And also provides other kickstarts for reference.


%prep
%setup -q -n "%{name}-%{commit}"
./autogen.sh

# Remove hash-bang from library files
find src/ -type f -name \*.py | xargs sed -i '1{\@^#@d}'


%build
%configure
make %{?_smp_mflags}


%install
%make_install


%check
%{__make} check TESTS="tests/package/check_python.test"


%files
%doc README.md LICENSE
%{_sbindir}/imgbase
%{_datadir}/%{name}/
%{python2_sitelib}/%{name}/
%{_mandir}/man8/imgbase.8*


%files kickstarts
%{_docdir}/%{name}


%changelog
* Mon Jul 21 2014 Fabian Deutsch <fabiand@redhat.com> - 0.1-0.8.git20140721.71b82f3
- Update to get missing files

* Mon Jul 21 2014 Fabian Deutsch <fabiand@redhat.com> - 0.1-0.7.git20140721.bb25471
- Update to a later snapshot
- Moves upstream spec into subdir

* Mon Jul 14 2014 Fabian Deutsch <fabiand@redhat.com> - 0.1-0.6.git20140714.8679e61
- Own datadir
- Add LICENSE file

* Wed Jul 09 2014 Fabian Deutsch <fabiand@redhat.com> - 0.1-0.5.git20140708.804811f
- Add autoconf and automake

* Wed Jul 09 2014 Fabian Deutsch <fabiand@redhat.com> - 0.1-0.4.git20140708.804811f
- Conditional requriement, based on the Fedora version

* Wed Jul 09 2014 Fabian Deutsch <fabiand@redhat.com> - 0.1-0.3.git20140708.804811f
- Fix package name: python-pexpect should be pexpect

* Wed Jul 09 2014 Fabian Deutsch <fabiand@redhat.com> - 0.1-0.2.git20140708.804811f
- Reorder and add dependencies

* Tue Jul 08 2014 Fabian Deutsch <fabiand@redhat.com> - 0.1-0.1.git20140708.804811f
- Initial package

