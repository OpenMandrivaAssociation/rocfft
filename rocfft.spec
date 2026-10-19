# HIP FFT library (TheRock 10.1)

Name:		rocfft
Version:	10.1.0
Release:	1
Summary:	HIP Fast Fourier Transform library
License:	MIT AND BSD-3-Clause
Group:		System/Libraries
URL:		https://github.com/ROCm/rocm-libraries
Source0:	https://github.com/ROCm/rocm-libraries/releases/download/therock-10.1/rocfft.tar.gz#/rocfft-%{version}.tar.gz
# HIP rtc compiles do not see a transitive declaration of strlen.
Patch0:		0001-cstring-symbol-name.patch

BuildRequires:	rocm-rpm-macros
BuildRequires:	cmake
BuildRequires:	ninja
BuildRequires:	rocm-cmake
BuildRequires:	hipcc
BuildRequires:	rocminfo
BuildRequires:	clang-tools
BuildRequires:	rocm-hip-devel
BuildRequires:	clang >= %{rocm_llvm_maj_ver}
# hiprtc is part of rocm-hip; ensure devel headers/cmake available
BuildRequires:	pkgconfig(libffi)
BuildRequires:	pkgconfig(sqlite3)


%description
rocFFT provides FFTs for HIP. Multi-ISA fat binary includes gfx803
(Polaris) on OpenMandriva where ROCr runtime support is restored.

%package devel
Summary:	Development files for rocfft
Group:		Development/C++
Requires:	%{name}%{?_isa} = %{version}-%{release}
Requires:	rocm-hip-devel
Provides:	rocfft-devel = %{EVRD}

%description devel
Headers and CMake package for rocfft.

%prep
%autosetup -n rocfft

export CXX=hipcc
export CC=clang
export ROCM_PATH=%{_prefix}
export HIP_PATH=%{_prefix}
CXXFLAGS=$(printf '%s' "%{optflags}" | sed -E 's/-mfpmath=[^ ]+//g; s/ -m[a-z0-9+.=]+//g')
export CXXFLAGS
export CFLAGS="$CXXFLAGS"
export LDFLAGS=$(printf '%s' "%{?__global_ldflags}" | sed -E 's/-mfpmath=[^ ]+//g; s/ -m[a-z0-9+.=]+//g')
%cmake %{rocm_cmake_fhs} %{rocm_cmake_gpu_targets_prim} \
	-DCMAKE_BUILD_TYPE=Release \
	-DCMAKE_CXX_COMPILER=hipcc \
	-DCMAKE_CXX_FLAGS="$CXXFLAGS" \
	-DBUILD_CLIENTS=OFF \
	-DBUILD_CLIENTS_TESTS=OFF \
	-DBUILD_CLIENTS_BENCH=OFF \
	-DBUILD_CLIENTS_SAMPLES=OFF \
	-DBUILD_SHARED_LIBS=ON \
	-DUSE_HIPRAND=OFF \
	-DROCFFT_BUILD_OFFLINE_TUNER=OFF \
	-DROCFFT_MPI_ENABLE=OFF \
-DSQLITE_USE_SYSTEM_PACKAGE=ON \
	-DROCM_PATH=%{_prefix} \
	-DCMAKE_PREFIX_PATH=%{_prefix} \
	-G Ninja

%build
%ninja_build -C build

%install
%ninja_install -C build
if [ -d %{buildroot}/usr/lib/cmake/rocfft ] && [ ! -d %{buildroot}%{_libdir}/cmake/rocfft ]; then
	mkdir -p %{buildroot}%{_libdir}/cmake
	mv %{buildroot}/usr/lib/cmake/rocfft %{buildroot}%{_libdir}/cmake/
	rmdir %{buildroot}/usr/lib/cmake 2>/dev/null || true
	rmdir %{buildroot}/usr/lib 2>/dev/null || true
fi

%files
%license LICENSE.md
%doc README.md
%exclude %{_docdir}/rocfft/LICENSE.md
%{_libdir}/librocfft.so.*
# AOT kernel caches + rtc helper under libdir/rocfft
%{_libdir}/rocfft/

%files devel
%{_includedir}/rocfft/
%{_libdir}/librocfft.so
%{_libdir}/cmake/rocfft/
