# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os
from spack_repo.builtin.build_systems.generic import Package
from spack.package import *


class Ollamabin(Package):
    """Install ollama from pre-built binaries."""

    homepage = "https://github.com/ollama/ollama"
    url = "https://github.com/ollama/ollama/releases/download/v0.3.9/ollama-linux-amd64.tgz"

    license("MIT", checked_by="brettviren")
    maintainers("brettviren")

    version("0.3.9", sha256="b0062fbccd46134818d9d59cfa3867ad6849163653cb1171bc852c5f379b0851")
    version("0.3.8", sha256="8e44f1ff4daad518eaf14bddc1ce98f6aaf2e26f55cab586360e586244e5a56d")
    version("0.3.7", sha256="4609dbde9a3242e2170f93aae9c1c0b35e424b24566ae0bb9f54f4082d832c0e")

    def install(self, spec, prefix):
        mkdirp(self.prefix)
        install_tree("bin", prefix.bin)
        install_tree("lib/ollama", prefix.lib)
        

    def setup_run_environment(self, env):
        env.prepend_path("LD_LIBRARY_PATH", self.prefix.lib);
        env.prepend_path("PATH", self.prefix.bin);

        tdir = os.environ["HOME"] + '/tmp'
        mkdirp(tdir)
        env.set("OLLAMA_TMPDIR", tdir);

        env.set("OLLAMA_HOST", "127.0.0.1:11434")  # default

        mdir = os.environ["HOME"] + '/.cache/ollama/models/bin'
        mkdirp(mdir)
        env.set("OLLAMA_MODELS", mdir)
