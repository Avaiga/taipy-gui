import typing as t
from ._default_config import default_config as default_config
from .config import Config as Config, ConfigParameter as ConfigParameter, StylekitVariables as StylekitVariables
from .extension.library import Element as Element, ElementLibrary as ElementLibrary
from .page import Page as Page
from .partial import Partial as Partial
from .state import State as State
from _typeshed import Incomplete
from flask import Flask

class _DoNotUpdate: ...

class Gui:
    on_action: Incomplete
    on_change: Incomplete
    on_init: Incomplete
    on_navigate: Incomplete
    on_exception: Incomplete
    on_status: Incomplete
    on_user_content: Incomplete
    def __init__(
        self,
        page: t.Optional[t.Union[str, Page]] = ...,
        pages: t.Optional[dict] = ...,
        css_file: t.Optional[str] = ...,
        path_mapping: t.Optional[dict] = ...,
        env_filename: t.Optional[str] = ...,
        libraries: t.Optional[t.List[ElementLibrary]] = ...,
        flask: t.Optional[Flask] = ...,
    ) -> None: ...
    @staticmethod
    def add_library(library: ElementLibrary) -> None: ...
    def __enter__(self): ...
    def __exit__(self, exc_type, exc_value, traceback): ...
    def add_page(self, name: str, page: t.Union[str, Page], style: t.Optional[str] = ...) -> None: ...
    def add_pages(self, pages: t.Optional[t.Union[t.Dict[str, t.Union[str, Page]], str]] = ...) -> None: ...
    def add_partial(self, page: t.Union[str, Page]) -> Partial: ...
    def load_config(self, config: Config) -> None: ...
    def broadcast(self, name: str, value: t.Any): ...
    def get_flask_app(self) -> Flask: ...
    state: Incomplete
    def run(
        self,
        allow_unsafe_werkzeug: bool = ...,
        async_mode: str = ...,
        change_delay: t.Optional[int] = ...,
        chart_dark_template: t.Optional[t.Dict[str, t.Any]] = ...,
        dark_mode: bool = ...,
        dark_theme: t.Optional[t.Dict[str, t.Any]] = ...,
        data_url_max_size: t.Optional[int] = ...,
        debug: bool = ...,
        extended_status: bool = ...,
        favicon: t.Optional[str] = ...,
        flask_log: bool = ...,
        host: str = ...,
        light_theme: t.Optional[t.Dict[str, t.Any]] = ...,
        margin: t.Optional[str] = ...,
        ngrok_token: str = ...,
        notification_duration: int = ...,
        propagate: bool = ...,
        run_browser: bool = ...,
        run_in_thread: bool = ...,
        run_server: bool = ...,
        single_client: bool = ...,
        system_notification: bool = ...,
        theme: t.Optional[t.Dict[str, t.Any]] = ...,
        time_zone: t.Optional[str] = ...,
        title: t.Optional[str] = ...,
        stylekit: bool = ...,
        stylekit_variables: StylekitVariables = ...,
        upload_folder: t.Optional[str] = ...,
        use_arrow: bool = ...,
        use_reloader: bool = ...,
        watermark: t.Optional[str] = ...,
        webapp_path: t.Optional[str] = ...,
        port: int = ...,
    ) -> t.Optional[Flask]: ...
    def stop(self) -> None: ...
