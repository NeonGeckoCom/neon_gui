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

import os
import sys
import unittest
import shutil

from os.path import join

from mock import mock

sys.path.append(os.path.dirname(os.path.dirname(__file__)))


class TestUtils(unittest.TestCase):
    def test_patch_config(self):
        import json
        import yaml
        from neon_gui.utils import use_neon_gui
        from neon_utils.configuration_utils import init_config_dir
        test_config_dir = os.path.join(os.path.dirname(__file__), "config")
        os.makedirs(test_config_dir, exist_ok=True)
        os.environ["XDG_CONFIG_HOME"] = test_config_dir
        use_neon_gui(init_config_dir)()

        with open(join(test_config_dir, "OpenVoiceOS", 'ovos.conf')) as f:
            ovos_conf = json.load(f)
        self.assertEqual(ovos_conf['submodule_mappings']['neon_gui'],
                         "neon_core")
        self.assertIsInstance(ovos_conf['module_overrides']['neon_core'], dict)
        from neon_gui.utils import patch_config
        test_config = {"new_key": {'val': True}}
        patch_config(test_config)
        conf_file = os.path.join(test_config_dir, 'neon',
                                 'neon.yaml')
        self.assertTrue(os.path.isfile(conf_file))
        with open(conf_file) as f:
            config = yaml.safe_load(f)

        self.assertTrue(config['new_key']['val'])
        shutil.rmtree(test_config_dir)
        os.environ.pop("XDG_CONFIG_HOME")

    @mock.patch('ovos_bus_client.apis.gui.extend_about_data')
    def test_add_about_data(self, extend_data):
        from neon_gui.utils import add_neon_about_data
        add_neon_about_data()
        extend_data.assert_called_once()
        data = extend_data.call_args[0][0]
        self.assertIsInstance(data, list)
        for i in data:
            self.assertIsInstance(i, dict)
            self.assertIsInstance(i['display_key'], str)
            self.assertIsInstance(i['display_value'], str)


if __name__ == '__main__':
    unittest.main()
