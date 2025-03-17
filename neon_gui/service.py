# NEON AI (TM) SOFTWARE, Software Development Kit & Application Framework
# All trademark and other rights reserved by their respective owners
# Copyright 2008-2025 Neongecko.com Inc.
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

from time import sleep
from tornado import ioloop
from threading import Thread, Event
from ovos_utils.log import LOG, log_deprecation
from ovos_gui.service import GUIService

from neon_gui.utils import update_gui_ip_address


def on_ready():
    LOG.info("GUI Service Ready")


def wrapped_ready_hook(ready_hook: callable):
    def wrapper():
        from neon_gui.utils import add_neon_about_data
        add_neon_about_data()
        LOG.info(f"Updated GUI About Data")
        ready_hook()
    return wrapper


def on_stopping():
    LOG.info('GUI service is shutting down...')


def on_error(e='Unknown'):
    LOG.error('GUI service failed to launch ({}).'.format(repr(e)))


def on_alive():
    LOG.debug("GUI client alive")


def on_started():
    LOG.debug("GUI client started")


class NeonGUIService(Thread, GUIService):
    def __init__(self, ready_hook=on_ready, error_hook=on_error,
                 stopping_hook=on_stopping, alive_hook=on_alive,
                 started_hook=on_started, gui_config=None, daemonic=False,):
        if gui_config:
            from neon_gui.utils import patch_config
            patch_config(gui_config)
        Thread.__init__(self)
        self.daemon = daemonic
        self.name = 'GUI'
        self.started = Event()
        ready_hook = wrapped_ready_hook(ready_hook)
        GUIService.__init__(self, alive_hook=alive_hook,
                            started_hook=started_hook, ready_hook=ready_hook,
                            error_hook=error_hook, stopping_hook=stopping_hook)

    @property
    def gui(self):
        log_deprecation("`self.gui` has been replaced by "
                        "`self.namespace_manager`", "2.0.0")
        return self.namespace_manager

    def run(self):
        self.status.set_started()
        GUIService.run(self)
        self.bus.on("ovos.wifi.setup.completed", update_gui_ip_address)
        self.started.set()

    def shutdown(self):
        LOG.info("GUI Service shutting down")
        self.status.set_stopping()
        self.namespace_manager.core_bus.close()
        self.bus.close()

        loop = ioloop.IOLoop.instance()
        loop.add_callback(loop.stop)
        sleep(1)
        loop.close()

        LOG.info("GUI Service stopped")
