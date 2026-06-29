# Local override of the builtin `jsonnet` (the reference C/C++ implementation).
#
# It is behaviorally identical to the builtin recipe (same versions, variants,
# and Makefile/CMake builders, inherited unchanged) but additionally `provides`
# the `libjsonnet` virtual. That lets the C/C++ Jsonnet be selected as an
# alternative engine to go-jsonnet for packages that depend on `libjsonnet`
# (e.g. phlex, phlexed). The builtin `jsonnet` already installs libjsonnet.so,
# libjsonnet++.so and the headers, so it satisfies the virtual as-is.
#
# The builders are re-imported into this module so Spack's builder lookup finds
# the builtin's customized MakefileBuilder/CMakeBuilder (PREFIX= install target,
# USE_SYSTEM_JSON, etc.) rather than the plain defaults.

from spack_repo.builtin.packages.jsonnet.package import (  # noqa: F401
    CMakeBuilder,
    Jsonnet as BuiltinJsonnet,
    MakefileBuilder,
)

from spack.package import *


class Jsonnet(BuiltinJsonnet):
    __doc__ = BuiltinJsonnet.__doc__

    provides("libjsonnet")
