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

from ovos_bus_client import Message
from ovos_utils.log import LOG
from ovos_utils.gui import extend_about_data


def patch_config(config: dict = None):
    """
    Write the specified speech configuration to the global config file
    :param config: Mycroft-compatible configuration override
    """
    from ovos_config.config import LocalConf
    from ovos_config.locations import USER_CONFIG

    config = config or dict()
    local_config = LocalConf(USER_CONFIG)
    local_config.update(config)
    local_config.store()


def use_neon_gui(func):
    """
    Wrapper to ensure call originates from neon_gui for stack checks.
    This is used for ovos-utils config platform detection which uses the stack
    to determine which module config to return.
    """
    def wrapper(*args, **kwargs):
        return func(*args, **kwargs)
    return wrapper


def add_neon_about_data():
    """
    Update the About menu in ovos-shell with Neon build information
    """
    from neon_utils.packaging_utils import get_package_version_spec
    from datetime import datetime

    # Get Core version as a date string (incl. leading '0' in month)
    try:
        core_version_parts = get_package_version_spec('neon_core').split('.')
        core_version_parts[1] = f'0{core_version_parts[1]}'\
            if len(core_version_parts[1]) == 1 else core_version_parts[1]
        core_version = '.'.join(core_version_parts)
    except ModuleNotFoundError:
        core_version = "Unknown"
    extra_data = [{"display_key": "Neon Core Version",
                  "display_value": core_version}]
    try:
        import json
        with open('/opt/neon/build_info.json') as f:
            build_info = json.load(f)
        image_recipe_time = datetime.fromtimestamp(
            build_info.get('image').get('time')).strftime('%Y-%m-%d')
        core_time = datetime.fromtimestamp(
            build_info.get('core').get('time')).strftime('%Y-%m-%d')

        installed_core_spec = build_info.get('core').get('version')
        extra_data.append({'display_key': 'Image Updated',
                           'display_value': image_recipe_time})
        extra_data.append({'display_key': 'Core Updated',
                           'display_value': core_time})

        if build_info.get('base_os'):
            base_os = build_info['base_os']['name']
            if build_info['base_os'].get('time', 'unknown') != 'unknown':
                time_str = datetime.fromtimestamp(
                    build_info['base_os'].get('time')).strftime('%Y-%m-%d')
                base_os = f'{base_os} ({time_str})'
            extra_data.append({'display_key': 'Base OS',
                               'display_value': base_os})
        if installed_core_spec != core_version:
            extra_data.append({'display_key': "Shipped Core Version",
                               'display_value': installed_core_spec})
    except FileNotFoundError:
        pass

    for pkg in ('neon_speech', 'neon_audio', 'neon_gui', 'neon_enclosure'):
        try:
            pkg_data = {"display_key": pkg,
                        "display_value": get_package_version_spec(pkg)}
        except ModuleNotFoundError:
            pkg_data = {"display_key": pkg,
                        "display_value": "Not Installed"}
        extra_data.append(pkg_data)

    LOG.debug(f"Updating GUI Data with: {extra_data}")
    extend_about_data(extra_data)


def update_gui_ip_address(_: Message):
    """
    Update the IP Address in the GUI on network changes.
    """
    from ovos_utils.network_utils import get_ip
    extra_data = [{"display_key": "Local Address",
                   "display_value": get_ip()}]
    LOG.debug("Updating GUI IP Address")
    extend_about_data(extra_data)
