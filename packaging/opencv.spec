#
# spec file for package opencv
#
# Copyright (c) 2012 SUSE LINUX Products GmbH, Nuernberg, Germany.
#
# All modifications and additions to the file contributed by third parties
# remain the property of their copyright owners, unless otherwise agreed
# upon. The license for this file, and modifications and additions to the
# file, is the same license as for the pristine package itself (unless the
# license for the pristine package is not an Open Source License, in which
# case the license is the MIT License). An "Open Source License" is a
# license that conforms to the Open Source Definition (Version 1.9)
# published by the Open Source Initiative.

# Please submit bugfixes or comments via http://bugs.opensuse.org/
#


%bcond_with ffmpeg

Name:           opencv
%define libname lib%{name}
%define soname  3_0
Version:        3.0.0beta
Release:        0
Summary:        Collection of algorithms for computer vision
License:        BSD-3-Clause
Group:          Development/Libraries/C and C++
Url:            http://%{name}.willowgarage.com/wiki/
Source0:        http://downloads.sourceforge.net/project/%{name}library/%{name}-unix/%{version}/OpenCV-%{version}.tar.bz2
BuildRoot:      %{_tmppath}/%{name}-%{version}-build
BuildRequires:  cmake
BuildRequires:  fdupes
#BuildRequires:  gstreamer-0_10-plugins-base-devel
BuildRequires: gstreamer-devel
BuildRequires:  libjpeg-devel
BuildRequires:  libtiff-devel
BuildRequires:  zlib-devel
BuildRequires:  qt5-qtwidgets-devel
BuildRequires:  qt5-plugin-generic-evdev
BuildRequires:  qt5-plugin-imageformat-gif
BuildRequires:  qt5-plugin-platform-linuxfb
BuildRequires:  qt5-plugin-platform-offscreen
BuildRequires:  qt5-plugin-platform-minimalegl
BuildRequires:  qt5-plugin-platform-minimal
BuildRequires:  qt5-plugin-platform-eglfs
BuildRequires:  qt5-plugin-imageformat-jpeg
BuildRequires:  qt5-plugin-platforminputcontext-ibus
BuildRequires:  qt5-plugin-imageformat-ico
BuildRequires:  qt5-qttest-devel
BuildRequires:  qt5-qtconcurrent-devel
Requires: qt5-qtwidgets

%description
OpenCV means Intel® Open Source Computer Vision Library. It is a collection of C
functions and a few C++ classes that implement some popular Image Processing and
Computer Vision algorithms.

%package -n %{libname}%{soname}
Summary:        Development files for using the OpenCV library
Group:          Development/Libraries/C and C++

%description -n %{libname}%{soname}
The Open Computer Vision Library is a collection of algorithms and sample code
for various computer vision problems. The library is compatible with IPL and
utilizes Intel Integrated Performance Primitives for better performance.

%package devel
Summary:        Development files for using the OpenCV library
Group:          Development/Libraries/C and C++
Requires:       %{libname}%{soname} = %{version}
Requires:       %{name} = %{version}

%description devel
This package contains the OpenCV C/C++ library and header files, as well as
documentation. It should be installed if you want to develop programs that will
use the OpenCV library.

%prep
%setup -qn OpenCV-%{version}

# Windows specific and with wrong end of line
rm -f doc/packaging.txt
#chmod +x samples/c/build_all.sh
#sed -i 's/\r$//' samples/c/adaptiveskindetector.cpp \
#                 samples/c/latentsvmdetect.cpp \
#                 samples/gpu/hog.cpp \
#                 samples/python/camshift.py

%build
export CFLAGS="%{optflags}"
export CXXFLAGS="%{optflags}"
mkdir build
cd build
cmake -DCMAKE_BUILD_TYPE=Release \
      -DCMAKE_INSTALL_PREFIX='%{_prefix}' \
      -DCMAKE_SKIP_RPATH=ON \
      -DBUILD_TESTS=OFF \
      -DINSTALL_C_EXAMPLES=ON \
      -DINSTALL_PYTHON_EXAMPLES=OFF \
      -DLIB_SUFFIX=$(echo %{_lib} | cut -b4-) \
      -DENABLE_OMIT_FRAME_POINTER=OFF \
      -DWITH_QT=ON \
      -DWITH_UNICAP=ON \
      -DWITH_XINE=ON \
      -DWITH_OPENGL=ON \
      -DENABLE_SSE2=ON \
      -DENABLE_SSE3=ON \
      -DENABLE_SSE41=ON \
      -DENABLE_SSE42=ON \
      -DENABLE_SSSE3=ON \
      -DWITH_IPP=OFF \
       ..

make %{?_smp_mflags} VERBOSE=1

%install
cd build
make DESTDIR=%{?buildroot:%{buildroot}} install/fast
%fdupes -s %{buildroot}%{_docdir}/%{name}-doc/examples

%clean
rm -rf %{buildroot}

%post   -n %{libname}%{soname} -p /sbin/ldconfig

%postun -n %{libname}%{soname} -p /sbin/ldconfig

%files -n %{libname}%{soname}
%manifest packaging/opencv.manifest
%defattr(-, root, root, 0755)
%{_libdir}/lib*.so.*
%{_libdir}/lib*.a

%files -n %{name}
%attr(0755, root, root) %{_bindir}/%{name}_*
%manifest packaging/opencv.manifest
%{_datadir}/OpenCV
%exclude %{_datadir}/OpenCV/OpenCVConfig*.cmake

%files devel
%manifest packaging/opencv.manifest
%{_includedir}/opencv
%{_includedir}/opencv2
%{_libdir}/lib*.so
%{_libdir}/pkgconfig/%{name}.pc
%{_datadir}/OpenCV/OpenCVConfig*.cmake

%changelog
