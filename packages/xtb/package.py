# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Xtb(CMakePackage):
    """Semi-empirical tight binding"""

    homepage = "https://xtb-docs.readthedocs.io/en/latest/contents.html"
    url      = "https://github.com/grimme-lab/xtb/archive/refs/tags/v6.6.0.tar.gz"

    version('6.6.0', sha256='1845a9ba71c7bdb414e14ef3dad676728c31a2a94b26303551da57704c78a3e3')
    version('6.5.1', sha256='8e5840469f9ef2c01ad5cb620481310ace62a7563c5d43375eb3d36463fc3add')
    version('6.4.1', sha256='cd7b6ec9b7963012ce71220a70773641f0d9e06e0691750a25b83e823510d1d7')

    depends_on('lapack')

    variant('openmp', description='Enables the use of OpenMP instructions',
            default=True)
    variant('shared', description='Enables the compilation of shared libraries',
            default=False)

    def cmake_args(self):

        args = []

        args.append(self.define_from_variant('WITH_OpenMP', 'openmp'))

        args.append(self.define_from_variant('BUILD_SHARED_LIBS', 'shared'))

        return args
