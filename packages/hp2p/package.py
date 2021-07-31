# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Hp2p(AutotoolsPackage):
    """HP2P (Heavy Peer To Peer) benchmark is a test which performs MPI
       Point-to-Point non-blocking communications between all MPI processes"""

    homepage = "https://github.com/cea-hpc/hp2p"
    git      = "https://github.com/cea-hpc/hp2p.git"

    version('3.3', tag='3.3')
    version('3.2', tag='3.2')
    version('3.1', tag='3.1')

    variant('vizualisation', default=True,
            description='Add dependencies to be able to postprocess the results')

    depends_on('automake', type=['build'])
    depends_on('autoconf', type=['build'])
    depends_on('libtool', type=['build'])
    depends_on('mpi')
    depends_on('python@2:2.99', type=['run'], when='vizualisation')
    depends_on('py-numpy', type=['run'], when='vizualisation')
    depends_on('py-matplotlib', type=['run'], when='vizualisation')

    def configure_args(self):
        return [
            'CC={0}'.format(self.spec['mpi'].mpicc),
            'CXX={0}'.format(self.spec['mpi'].mpicxx),
        ]
