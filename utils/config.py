import os
import sys
import yaml
from .debug import e_print


class Config:
    @staticmethod
    def load():
        config_file = sys.path[0] + "/config.yml"
        if not os.path.exists(config_file):
            with open(config_file, 'w') as yaml_file:
                pass
        with open(config_file) as yaml_file:
            try:
                data = yaml.load(yaml_file, Loader=yaml.FullLoader)
                if data is None:
                    data = dict()
            except Exception as err:
                e_print('read config file failed, exception: ', err)
                exit(-1)
            return data

    @staticmethod
    def store(data):
        config_file = sys.path[0] + "/config.yml"
        with open(config_file, 'w') as yaml_file:
            yaml_file.write(yaml.dump(data, default_flow_style=False))
