# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os
import shutil

from spack import *


class Vasp(Package, CudaPackage):
    """VASP is a plane wave electronic structure code."""

    homepage = "http://www.vasp.at"
    url      = "fake_url.tar.gz"
    licensed = True

    version('5.4.4',
            sha256='5bd2449462386f01e575f9adf629c08cb03a13142806ffb6a71309ca4431cfb3',
            url='file://%s/vasp.5.4.4.tar.gz' % os.getcwd())

    variant('mpi', default=True, description='Build with MPI support')

    depends_on('blas')
    depends_on('lapack')
    depends_on('fftw-api@3:')
    depends_on('mpi', when='+mpi')
    depends_on('scalapack', when='+mpi')
    depends_on('magma', when='+cuda')
    
    parallel = False

    def install(self, spec, prefix):
        arch_file = join_path('arch', 'makefile.include.linux_{0}'.format(
            'intel' if spec.compiler.name == 'intel' else 'gnu'))
        shutil.copy(arch_file, 'makefile.include')

        args = {
            'BLAS': spec['blas'].libs.ld_flags,
            'LAPACK': spec['lapack'].libs.ld_flags,
            'SCALAPACK': spec['scalapack'].libs.ld_flags,
            'FFTW': spec['fftw-api'].libs.directories,
            'MPI_INC': spec['mpi'].prefix.include,
            'FC': spec['mpi'].mpifc,
            'CC': os.environ['CC'],
            'CC_LIB': os.environ['CC'],
            'CXX':  os.environ['CXX'],
            'CXX_PARS':  os.environ['CXX'],
        }

        _extra_nvcc_options = ''
        if self.compiler.name == 'intel':
            _extra_nvcc_options = '  -gxx-name=/usr/bin/g++'

        if '+cuda' in spec:
            cuda_arch = [x for x in spec.variants['cuda_arch'].value if x]
            args['CUDA_ROOT'] = spec['cuda'].prefix
            args['NVCC'] = '$(CUDA_ROOT)/bin/nvcc -ccbin={0}{1}'.format(
                os.environ['CXX'],
                _extra_nvcc_options,
            )

        for arg in args:
            filter_file(r'(?ms)(^{0}\s*[?:+]?=).*?(?<! \\)$'.format(arg),
                        r'\1 {0}'.format(args[arg]),
                        'makefile.include')

        if spec.satisfies('%intel@15:'):
            filter_file(r'-openmp', r'-qopenmp', 'makefile.include')

        make('all')
        if '+cuda' in spec:
            make('gpu')
            make('gpu_ncl')
        shutil.copytree('bin', spec.prefix.bin)
