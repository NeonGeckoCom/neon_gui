# NEON AI (TM) SOFTWARE, Software Development Kit & Application Framework
# All trademark and other rights reserved by their respective owners
# Copyright 2008-2022 Neongecko.com Inc.
# Contributors: Daniel McKnight, Guy Daniels, Elon Gasper, Richard Leeds,
# Regina Bloomstine, Casimiro Ferreira, Andrii Pernatii, Kirill Hrymailo
# BSD-3 License
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
# 1. Redistributions of source code must retain the above copyright notice,
#    this list of conditions and the following disclaimer.
# 2. Redistributions in binary form must reproduce the above copyright notice,
#    this list of conditions and the following disclaimer in the documentation
#    and/or other materials provided with the distribution.
# 3. Neither the name of the copyright holder nor the names of its
#    contributors may be used to endorse or promote products derived from this
#    software without specific prior written permission.
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO,
# THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR
# PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR
# CONTRIBUTORS  BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL,
# EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO,
# PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA,
# OR PROFITS;  OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF
# LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING
# NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
# SOFTWARE,  EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

import asyncio

from time import sleep
from tornado import ioloop
from threading import Thread
from neon_utils.logger import LOG

from mycroft.gui.service import GUIService


def on_ready():
    LOG.info("GUI Service Ready")
    from neon_gui.utils import add_neon_about_data
    add_neon_about_data()
    LOG.info(f"Updated GUI About Data")


class NeonGUIService(Thread, GUIService):
    def __init__(self, gui_config=None, daemonic=False):
        if gui_config:
            from neon_gui.utils import patch_config
            patch_config(gui_config)
        Thread.__init__(self)
        self.setDaemon(daemonic)
        GUIService.__init__(self, ready_hook=on_ready)

    def run(self):
        GUIService.run(self)

    def shutdown(self):
        LOG.info("GUI Service shutting down")
        self.status.set_stopping()
        # self.gui.gui_bus.stop()

        loop = ioloop.IOLoop.instance()
        loop.add_callback(loop.stop)
        sleep(1)
        loop.close()

        LOG.info("GUI Service stopped")
