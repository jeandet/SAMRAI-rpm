%global snaprel %{nil}

Name: SAMRAI
%define v_major 3
%define v_minor 14
%define v_patch 0
Version: %{v_major}.%{v_minor}.%{v_patch}
%define src_dir %{name}-%{version}
Release: 0%{?dist}
Summary: A general purpose library and file format for storing scientific data
License: GPLv2.1
Group: System Environment/Libraries
URL: https://github.com/LLNL/SAMRAI
Source0: https://github.com/LLNL/SAMRAI
BuildRequires: gcc-gfortran
BuildRequires: gcc
BuildRequires: gcc-c++
BuildRequires: cmake
BuildRequires: git
BuildRequires: hdf5-openmpi-devel
BuildRequires: openmpi-devel
BuildRequires: m4
BuildRequires: boost-openmpi-devel

Requires: openmpi
Requires: hdf5-openmpi
Requires: boost-openmpi

%description
SAMRAI (Structured Adaptive Mesh Refinement Application Infrastructure) is an object-oriented C++ software library
that enables exploration of numerical, algorithmic, parallel computing, and software issues associated with applying
structured adaptive mesh refinement (SAMR) technology in large-scale parallel application development.
  SAMRAI provides software tools for developing SAMR applications that involve coupled physics models, sophisticated
numerical solution methods, and which require high-performance parallel computing hardware.
  SAMRAI enables integration of SAMR technology into existing codes and simplifies the exploration of SAMR methods
in new application domains.

%package devel
Summary: SAMRAI development files
Group: Development/Libraries
%description devel
SAMRAI development headers and libraries.

%package openmpi
Summary: SAMRAI openmpi version
Group: Development/Libraries
Requires: openmpi
%description openmpi

%prep
rm -rf %{src_dir}
git clone --recursive %{url}.git %{src_dir}
cd %{src_dir}
git checkout tags/v-%{v_major}-%{v_minor}-%{v_patch}



%build
%define dobuild() \
cd %{src_dir} \
mkdir $MPI_COMPILER; \
cd $MPI_COMPILER;  \
export CXXFLAGS="%{optflags} -Wl,--as-needed"; \
%cmake -DINSTALL_CMAKE_DIR="%{_libdir}/cmake/" -DENABLE_COPY_HEADERS=ON -DCMAKE_C_COMPILER="mpicc" -DCMAKE_CXX_COMPILER="mpic++" -DCMAKE_FORTRAN_COMPILER="mpif90" -DCMAKE_BUILD_TYPE=Release -DCMAKE_INSTALL_BINDIR="$MPI_BIN" -DCMAKE_INSTALL_LIBDIR="$MPI_LIB" -DPYTHON_SITE_PACKAGES="$MPI_PYTHON_SITEARCH" .. ; \
make %{?_smp_mflags}; \
cd .. ; \


# Set compiler variables to MPI wrappers
export CC=mpicc
export CXX=mpicxx
export FC=mpif90
export F77=mpif77

## Build OpenMPI version
%{_openmpi_load}
%dobuild
%{_openmpi_unload}

%check
%define docheck() \
export  CTEST_OUTPUT_ON_FAILURE=1; \
cd %{src_dir}/$MPI_COMPILER ; \
ctest -V %{?_smp_mflags}; \
cd .. ; \


## Test OpenMPI version
%{_openmpi_load}
%docheck
%{_openmpi_unload}


%install

## Install OpenMPI version
%{_openmpi_load}
make -C %{src_dir}/$MPI_COMPILER install DESTDIR=%{buildroot} INSTALL="install -p" CPPROG="cp -p"
%{_openmpi_unload}

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig


%files

%files openmpi
%{_libdir}/*

%files devel
%{_includedir}/*
%{_datarootdir}/SAMRAI/cmake/*



%changelog

* Thu Sep 17 2019 Alexis Jeandet <alexis.jeandet@member.fsf.org> - 3.14.0-0
- Now follows SAMRAI releases

* Thu Nov 8 2018 Alexis Jeandet <alexis.jeandet@member.fsf.org> - 1.0.0-4
- Added debuginfo packages

* Wed Oct 3 2018 Alexis Jeandet <alexis.jeandet@member.fsf.org> - 1.0.0-3
- Switch to upstream repository feature/blt branch

* Sat Sep 8 2018 Alexis Jeandet <alexis.jeandet@member.fsf.org> - 1.0.0-0
- First setup
