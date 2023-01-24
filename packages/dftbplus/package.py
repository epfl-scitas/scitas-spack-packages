# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os

from spack import *


class Dftbplus(CMakePackage):
    """DFTB+ is an implementation of the
    Density Functional based Tight Binding (DFTB) method,
    containing many extensions to the original method."""

    homepage = "https://www.dftbplus.org"
    url      = "https://github.com/dftbplus/dftbplus/archive/22.1.tar.gz"

    version('22.2', sha256='ca69a5e21bf9071179c5a2c57d89cdcbb0543e771661ac5e8be584fafa4c61df')
    version('22.1', sha256='f0fc9a076aa2d7be03c31a3a845d8151fc0cc0b1d421e11c37044f78a42abb33')
    # Disabling the old version so we can use CMakePackage
    #version('19.1', sha256='4d07f5c6102f06999d8cfdb1d17f5b59f9f2b804697f14b3bc562e3ea094b8a8')

    resource(name='slakos',
             url='https://github.com/dftbplus/testparams/archive/dftbplus-18.2.tar.gz',
             sha256='bd191b3d240c1a81a8754a365e53a78b581fc92eb074dd5beb8b56a669a8d3d1',
             destination='external/slakos',
             when='@18.2:')

    variant('mpi', default=True,
            description="Build an MPI-parallelised version of the code.")

    variant('openmp', default=False,
            description="Build an OpenMP-parallelised version of the code.")

    variant('gpu', default=False,
            description="Use the MAGMA library "
            "for GPU accelerated computation")

    variant('elsi', default=False,
            description="Use the ELSI library for large scale systems. "
            "Only has any effect if you build with '+mpi'")

    variant('sockets', default=False,
            description="Whether the socket library "
            "(external control) should be linked")

    variant('arpack', default=False,
            description="Use ARPACK for excited state DFTB functionality")

    variant('transport', default=False,
            description="Whether transport via libNEGF should be included. "
            "Only affects parallel build. "
            "(serial version is built without libNEGF/transport)")

    # Disabling it for now (see next comment)
    # variant('dftd3', default=False,
    #         description="Use DftD3 dispersion library "
    #         "(if you need this dispersion model)")

    depends_on('lapack')
    depends_on('blas')
    depends_on('scalapack', when="+mpi")
    depends_on('mpi', when="+mpi")
    depends_on('elsi', when="+elsi")
    depends_on('magma', when="+gpu")
    depends_on('arpack-ng', when="+arpack")
    # simple-dftd3 was added on spack 0.19
    # depends_on('simple-dftd3', when="+dftd3")

    def cmake_args(self):

        options = []

        if '+mpi' in self.spec:
            options.append('-DWITH_MPI=ON')
            options.append('-DSCALAPACK_LIBRARY={0}'.format(self.spec['scalapack'].libs.joined(';')))

            if '+elsi' in self.spec:
                options.append('-DWITH_ELSI=ON')

        if '+openmp' in self.spec:
            options.append('-DWITH_OMP=ON')

        if '+gpu' in self.spec:
            options.append('-DWITH_GPU=ON')

        if '+sockets' in self.spec:
            options.append('-DWITH_SOCKETS=ON')

        if '+transport' in self.spec:
            options.append('-DWITH_TRANSPORT=ON')

        if '+arpack' in self.spec:
            options.append('-DWITH_ARPACK=ON')

        # if '+dftd3' in self.spec:
        #     options.append('-DWITH_SDFTD3=ON')

        return options

