# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os
from spack.package import *

class Ollamalux(Package):
    """Install luixiao0/ollama from pre-built binaries."""

    homepage = "https://github.com/luixiao0/ollama"
    url = "https://github.com/luixiao0/ollama/releases/download/v1.35.1/ollama"

    license("MIT", checked_by="brettviren")
    maintainers("brettviren")

    version("1.35.1", sha256="10c49b200ab81f8f7f5b942adbb476c263b45a1e856f35f02303390e63382ad1", expand=False)
    def install(self, spec, prefix):
        mkdirp(self.prefix.bin)
        path = join_path(prefix.bin, "ollama")
        install("ollama", path)
        chmod = which("chmod")
        chmod("+x", path)


    def setup_run_environment(self, env):
        env.prepend_path("PATH", self.prefix.bin);

        tdir = os.environ["HOME"] + '/tmp'
        mkdirp(tdir)
        env.set("OLLAMA_TMPDIR", tdir);

        env.set("OLLAMA_HOST", "127.0.0.1:11435")  # default + 1

        mdir = os.environ["HOME"] + '/.cache/ollama/models/lux'
        mkdirp(mdir)
        env.set("OLLAMA_MODELS", mdir)

