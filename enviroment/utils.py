import io
import yaml

def init_properties(path_config):
    with open(path_config) as file:
        return yaml.load(file, Loader=yaml.FullLoader)