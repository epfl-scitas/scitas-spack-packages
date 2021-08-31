# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PySpython(PythonPackage):
    """Singularity Python (spython) is the Python API for working with Singularity
    containers."""

    homepage = "https://singularityhub.github.io/singularity-cli/"
    url      = "https://files.pythonhosted.org/packages/e6/01/3df4e95cc753153bf49593da9b54889416316cdb36d37b7233e82e553943/spython-0.1.15.tar.gz"

    version('0.1.15', sha256='7674b8b9b3b2e723e5754849985bd668c8056f9d79ff019ba6f4237c70e15367')

    #depends_on('python@2.X:2.Y,3.Z:', type=('build', 'run'))
    depends_on('py-setuptools', type='build')
    depends_on('singularity@3.5.2:', type=('build', 'run'))
