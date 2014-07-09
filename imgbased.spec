
%global commit 804811f04355f57cd2ee4ca50d03ed8b9a6ba4bc
%global shortcommit %(c=%{commit}; echo ${c:0:7})
%global commitdate 20140708
%global gitversion .git%{commitdate}.%{shortcommit}
%global source https://github.com/fabiand/%{name}/archive/%{commit}/%{name}-%{version}-%{shortcommit}.tar.gz

Summary:        Tools to work with an image based rootfs
Name:           imgbased
Version:        0.1
Release:        0.2%{?gitversion}%{?dist}

License:        GPLv2+
URL:            https://github.com/fabiand/%{name}
Source0:        %{?source}
BuildArch:      noarch

BuildRequires:  python2-devel
BuildRequires:  python3-devel
BuildRequires:  asciidoc
BuildRequires:  pylint
BuildRequires:  pyflakes
BuildRequires:  python-pep8
BuildRequires:  pyhon-pexpect

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
%doc README.md
%{_sbindir}/imgbase
%{_datadir}/%{name}/hooks.d/
%{python2_sitelib}/%{name}/
%{_mandir}/man8/imgbase.8*


%files kickstarts
%{_docdir}/%{name}


%changelog
* Wed Jul 09 2014 Fabian Deutsch <fabiand@redhat.com> - 0.1-0.2.git20140708.804811f
- Reorder and add dependencies

* Tue Jul 08 2014 Fabian Deutsch <fabiand@redhat.com> - 0.1-0.1.git20140708.804811f
- Initial package

