import os
import sys
import yaml


class Config:
    @staticmethod
    def load():
        config_file = sys.path[0] + "/config.yaml"
        if not os.path.exists(config_file):
            with open(config_file, 'w') as yaml_file:
                pass
        with open(config_file) as yaml_file:
            try:
                data = yaml.load(yaml_file)
            except:
                data = {}
            return data

    @staticmethod
    def store(data):
        config_file = sys.path[0] + "/config.yaml"
        with open(config_file, 'w') as yaml_file:
            yaml_file.write(yaml.dump(data, default_flow_style=False))
