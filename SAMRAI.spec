# Patch version?

%global snaprel %{nil}

# NOTE: Try not to release new versions to released versions of Fedora

# You need to recompile all users of HDF5 for each version change

Name: SAMRAI

Version: 1.0.0

%define src_dir   %{name}-%{version}

Release: 0%{?dist}

Summary: A general purpose library and file format for storing scientific data

License: GPLv2.1

Group: System Environment/Libraries

URL: https://github.com/monwarez/SAMRAI

BuildRequires: gcc-gfortran, gcc, gcc-c++, cmake


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

Requires: %{name}%{?_isa} = %{version}-%{release}

Requires: hdf5-devel%{?_isa}

%description devel

SAMRAI development headers and libraries.


%package openmpi

Summary: SAMRAI openmpi libraries

Group: Development/Libraries

BuildRequires: openmpi-devel, hdf5-openmpi-devel

%description openmpi

SAMRAI parallel openmpi libraries

%package openmpi-devel

Summary: SAMRAI openmpi development files

Group: Development/Libraries

Requires: %{name}-openmpi%{?_isa} = %{version}-%{release}

Requires: openmpi-devel%{?_isa}

%description openmpi-devel

SAMRAI parallel openmpi development files





%prep

git clone %{URL} ${SAMRAI_SRCDIR} --branch add-install --recursive %{src_dir}
cd %{src_dir}


# Modify low optimization level for gnu compilers

%define dobuild() \
mkdir $MPI_COMPILER; \
cd $MPI_COMPILER;  \
export CXXFLAGS="%{optflags} -Wl,--as-needed"; \
%cmake -DINSTALL_CMAKE_DIR="%{_libdir}/cmake/" -DCMAKE_C_COMPILER="mpicc" -DCMAKE_CXX_COMPILER="mpic++" -DCMAKE_FORTRAN_COMPILER="mpif90" -DCMAKE_BUILD_TYPE=Release .. ; \
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

%changelog

* Sat Sep 8 2018 Alexis Jeandet <alexis.jeandet@member.fsf.org> - 1.0.0-0

- First setup