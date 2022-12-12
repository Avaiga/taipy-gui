# Copyright 2022 Avaiga Private Limited
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may not use this file except in compliance with
# the License. You may obtain a copy of the License at
#
#        http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software distributed under the License is distributed on
# an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the License for the
# specific language governing permissions and limitations under the License.

import argparse
import os
import re
import typing as t
import warnings
from importlib.util import find_spec

import pytz
import tzlocal
from dotenv import dotenv_values
from werkzeug.serving import is_running_from_reloader

from taipy.logger._taipy_logger import _TaipyLogger

from ._page import _Page
from .partial import Partial
from .utils import _is_in_notebook

ConfigParameter = t.Literal[
    "allow_unsafe_werkzeug",
    "async_mode",
    "change_delay",
    "dark_mode",
    "dark_theme",
    "data_url_max_size",
    "debug",
    "extended_status",
    "favicon",
    "flask_log",
    "host",
    "light_theme",
    "margin",
    "ngrok_token",
    "notification_duration",
    "propagate",
    "run_browser",
    "run_in_thread",
    "run_server",
    "single_client",
    "system_notification",
    "theme",
    "time_zone",
    "title",
    "upload_folder",
    "use_arrow",
    "use_reloader",
    "watermark",
    "port",
]

Config = t.TypedDict(
    "Config",
    {
        "allow_unsafe_werkzeug": bool,
        "async_mode": str,
        "change_delay": t.Optional[int],
        "dark_mode": bool,
        "dark_theme": t.Optional[t.Dict[str, t.Any]],
        "data_url_max_size": t.Optional[int],
        "debug": bool,
        "extended_status": bool,
        "favicon": t.Optional[str],
        "flask_log": bool,
        "host": str,
        "light_theme": t.Optional[t.Dict[str, t.Any]],
        "margin": t.Optional[str],
        "ngrok_token": str,
        "notification_duration": int,
        "propagate": bool,
        "run_browser": bool,
        "run_in_thread": bool,
        "run_server": bool,
        "single_client": bool,
        "system_notification": bool,
        "theme": t.Optional[t.Dict[str, t.Any]],
        "time_zone": t.Optional[str],
        "title": t.Optional[str],
        "upload_folder": t.Optional[str],
        "use_arrow": bool,
        "use_reloader": bool,
        "watermark": t.Optional[str],
        "port": int,
    },
    total=False,
)


class _Config(object):

    __RE_PORT_NUMBER = re.compile(
        r"^([0-9]{1,4}|[1-5][0-9]{4}|6[0-4][0-9]{3}|65[0-4][0-9]{2}|655[0-2][0-9]|6553[0-5])$"
    )

    def __init__(self):
        self.pages: t.List[_Page] = []
        self.routes: t.List[str] = []
        self.partials: t.List[Partial] = []
        self.partial_routes: t.List[str] = []
        self.config: Config = {}

    def _load(self, config: Config) -> None:
        self.config.update(config)
        # Check that the user timezone configuration setting is valid
        self.get_time_zone()

    def _get_config(self, name: ConfigParameter, default_value: t.Any) -> t.Any:  # pragma: no cover
        if name in self.config and self.config[name] is not None:
            if default_value is not None and not isinstance(self.config[name], type(default_value)):
                try:
                    return type(default_value)(self.config[name])
                except Exception as e:
                    warnings.warn(
                        f'app_config "{name}" value "{self.config[name]}" is not of type {type(default_value)}\n{e}'
                    )
                    return default_value
            return self.config[name]
        return default_value

    def get_time_zone(self) -> t.Optional[str]:
        tz = self.config.get("time_zone")
        if tz is None or tz == "client":
            return tz
        if tz == "server":
            # return python tzlocal IANA Time Zone
            return str(tzlocal.get_localzone())
        # Verify user defined IANA Time Zone is valid
        if tz not in pytz.all_timezones_set:
            raise Exception(
                "Time Zone configuration is not valid. Mistyped 'server', 'client' options or invalid IANA Time Zone"
            )
        # return user defined IANA Time Zone (https://en.wikipedia.org/wiki/List_of_tz_database_time_zones)
        return tz

    def _init_argparse(self):
        parser = argparse.ArgumentParser()
        parser.add_argument("-P", "--port", nargs="?", default="", const="", help="Specify server port")
        parser.add_argument("-H", "--host", nargs="?", default="", const="", help="Specify server host")

        parser.add_argument("--ngrok-token", nargs="?", default="", const="", help="Specify NGROK Authtoken")

        debug_group = parser.add_mutually_exclusive_group()
        debug_group.add_argument("--debug", help="Turn on debug", action="store_true")
        debug_group.add_argument("--no-debug", help="Turn off debug", action="store_true")

        reloader_group = parser.add_mutually_exclusive_group()
        reloader_group.add_argument("--use-reloader", help="Auto reload on code changes", action="store_true")
        reloader_group.add_argument("--no-reloader", help="No reload on code changes", action="store_true")

        args, unknown_args = parser.parse_known_args()
        self._handle_argparse(args)

    def _handle_argparse(self, args):  # pragma: no cover
        config = self.config
        if args.port:
            if not _Config.__RE_PORT_NUMBER.match(args.port):
                warnings.warn("Port value for --port option is not valid")
            else:
                config["port"] = int(args.port)
        if args.host:
            config["host"] = args.host
        if args.debug:
            config["debug"] = True
        if args.no_debug:
            config["debug"] = False
        if args.use_reloader:
            config["use_reloader"] = True
        if args.no_reloader:
            config["use_reloader"] = False
        if args.ngrok_token:
            config["ngrok_token"] = args.ngrok_token

    def _build_config(self, root_dir, env_filename, kwargs):  # pragma: no cover
        config = self.config
        env_file_abs_path = env_filename if os.path.isabs(env_filename) else os.path.join(root_dir, env_filename)
        # Load keyword arguments
        for key, value in kwargs.items():
            key = key.lower()
            if value is not None and key in config:
                try:
                    config[key] = value if config[key] is None else type(config[key])(value)  # type: ignore
                except Exception as e:
                    warnings.warn(
                        f"Invalid keyword arguments value in Gui.run {key} - {value}. Unable to parse value to the correct type.\n{e}"
                    )
        # Load config from env file
        if os.path.isfile(env_file_abs_path):
            for key, value in dotenv_values(env_file_abs_path).items():
                key = key.lower()
                if value is not None and key in config:
                    try:
                        config[key] = value if config[key] is None else type(config[key])(value)  # type: ignore
                    except Exception as e:
                        warnings.warn(
                            f"Invalid env value in Gui.run: {key} - {value}. Unable to parse value to the correct type.\n{e}"
                        )
        # Load from system arguments
        self._init_argparse()

        # Taipy-config
        if find_spec("taipy") and find_spec("taipy.config"):
            from taipy.config import Config as TaipyConfig

            try:
                section = TaipyConfig.unique_sections["gui"]
                self.config.update(section._to_dict())
            except KeyError:
                warnings.warn("taipy-config section for taipy-gui is not initialized")

    def __log_outside_reloader(self, logger, msg):
        if not is_running_from_reloader():
            logger.info(msg)

    def resolve(self):
        app_config = self.config
        logger = _TaipyLogger._get_logger()
        # Special config for notebook runtime
        if _is_in_notebook() or app_config["run_in_thread"] and not app_config["single_client"]:
            app_config["single_client"] = True
            self.__log_outside_reloader(logger, "Running in 'single_client' mode in notebook environment")

        if app_config["run_server"] and app_config["ngrok_token"] and app_config["use_reloader"]:
            app_config["use_reloader"] = False
            self.__log_outside_reloader(
                logger, "'use_reloader' parameter will not be used when 'ngrok_token' parameter is available"
            )

        if app_config["use_reloader"] and not app_config["debug"]:
            app_config["debug"] = True
            self.__log_outside_reloader(logger, "application is running in 'debug' mode")

        if app_config["debug"] and not app_config["allow_unsafe_werkzeug"]:
            app_config["allow_unsafe_werkzeug"] = True
            self.__log_outside_reloader(logger, "'allow_unsafe_werkzeug' has been set to True")

        if app_config["debug"] and app_config["async_mode"] != "threading":
            app_config["async_mode"] = "threading"
            self.__log_outside_reloader(
                logger,
                "'async_mode' parameter has been overridden to 'threading'. Using Flask built-in development server with debug mode",
            )


def _register_gui_config():
    if not find_spec("taipy") or not find_spec("taipy.config"):
        return
    from copy import copy

    from taipy.config import Config as TaipyConfig
    from taipy.config import UniqueSection

    from ._default_config import default_config

    class _GuiSection(UniqueSection):

        name = "gui"

        def __init__(self, property_list: t.Optional[t.List] = None, **properties):
            self._property_list = property_list
            super().__init__(**properties)

        def __copy__(self):
            return _GuiSection(property_list=copy(self._property_list), **copy(self._properties))

        def _to_dict(self):
            as_dict = {}
            as_dict.update(self._properties)
            return as_dict

        @classmethod
        def _from_dict(cls, as_dict: t.Dict[str, t.Any], *_):
            return _GuiSection(property_list=list(default_config), **as_dict)

        def _update(self, as_dict: t.Dict[str, t.Any]):
            if self._property_list:
                as_dict = {k: v for k, v in as_dict.items() if k in self._property_list}
            self._properties.update(as_dict)

        @staticmethod
        def _configure(**properties):
            section = _GuiSection(property_list=list(default_config), **properties)
            TaipyConfig._register(section)
            return TaipyConfig.unique_sections[_GuiSection.name]

    TaipyConfig._register_default(_GuiSection(property_list=list(default_config)))
    TaipyConfig.configure_gui = _GuiSection._configure
