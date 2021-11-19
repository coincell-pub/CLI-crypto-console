# Copyright (c) 2021, coincell
# All rights reserved.

# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:

# 1. Redistributions of source code must retain the above copyright notice, this
#    list of conditions and the following disclaimer.
# 2. Redistributions in binary form must reproduce the above copyright notice,
#    this list of conditions and the following disclaimer in the documentation
#    and/or other materials provided with the distribution.

# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
# ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE LIABLE FOR
# ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
# (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
# LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND
# ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
# SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

# The views and conclusions contained in the software and documentation are those
# of the authors and should not be interpreted as representing official policies,
# either expressed or implied, of the FreeBSD Project.

import yaml
from exceptions import KeyMissingConfigException
from utils import decrypt_file

class ExchangeConfig:
    def __init__(self, api_key, api_secret):
        self.api_key = api_key
        self.api_secret = api_secret

class ConfigManager:
    def __init__(self):
        pass

    def _ensure_key_is_present(self, config, key):
        if key not in config:
            raise KeyMissingConfigException(key)

    def _process_config(self, config):
        self._ensure_key_is_present(config, 'exchanges')
        self._ensure_key_is_present(config, 'database')
        self._ensure_key_is_present(config['database'], 'path')
        exchanges = {}
        if len(config['exchanges']) == 0:
            raise ConfigException('Exchange list can\'t be empty')
        for exchange in config['exchanges']:
            self._ensure_key_is_present(exchange, 'api_key')
            self._ensure_key_is_present(exchange, 'api_secret')
            self._ensure_key_is_present(exchange, 'name')
            exchanges[exchange['name']] = ExchangeConfig(
                exchange['api_key'],
                exchange['api_secret']
            )
        self.fiat_currency = None
        for key, value in config.get('metadata', {}).items():
            if key == 'fiat_currency':
                self.fiat_currency = value
        self.history_path = config.get('history', {}).get('path', None)
        self.exchanges = exchanges
        self.database_path = config['database']['path']

    def load(self, config_file):
        config = yaml.safe_load(open(config_file))
        self._process_config(config)

    def load_encrypted(self, config_file, passphrase):
        config = yaml.safe_load(decrypt_file(config_file, passphrase))
        self._process_config(config)

