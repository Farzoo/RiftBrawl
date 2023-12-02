import json
from typing import Any

from resources.resources_registry import ResourcesRegistry


class SettingsLoader:

    @staticmethod
    def load_settings_from_json(filepath: str) -> ResourcesRegistry.ResourceRegistryBuilder[str, Any]:
        try:
            with open(filepath, 'r') as file:
                data = json.load(file)
                settings = ResourcesRegistry.ResourceRegistryBuilder()
                for setting_name, setting_data in data.items():
                    settings.register(setting_name, setting_data)
                return settings
        except Exception as e:
            raise ValueError("Invalid json file: {}".format(str(e)))
