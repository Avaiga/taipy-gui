import pathlib
import typing as t
from .config import Config, ConfigParameter, StylekitVariables as StylekitVariables
from .data.data_accessor import _DataAccessor as _DataAccessor
from .extension.library import ElementLibrary
from .page import Page
from .partial import Partial
from .state import State
from .types import _WsType
from .utils import _TaipyBase
from _typeshed import Incomplete
from flask import Flask
from types import FrameType

class _DoNotUpdate:
    def __repr__(self): ...

class Gui:
    __root_page_name: str
    __env_filename: str
    __UI_BLOCK_NAME: str
    __MESSAGE_GROUPING_NAME: str
    __ON_INIT_NAME: str
    __ARG_CLIENT_ID: str
    __INIT_URL: str
    __JSX_URL: str
    __CONTENT_ROOT: str
    __UPLOAD_URL: str
    _EXTENSION_ROOT: str
    __USER_CONTENT_URL: str
    __SELF_VAR: str
    __DO_NOT_UPDATE_VALUE: Incomplete
    __RE_HTML: Incomplete
    __RE_MD: Incomplete
    __RE_PAGE_NAME: Incomplete
    __reserved_routes: t.List[str]
    __LOCAL_TZ: Incomplete
    __extensions: t.Dict[str, t.List[ElementLibrary]]
    __frame: Incomplete
    __default_module_name: Incomplete
    _path_mapping: Incomplete
    _flask: Incomplete
    __css_file: Incomplete
    _config: Incomplete
    __content_accessor: Incomplete
    _accessors: Incomplete
    __state: Incomplete
    __bindings: Incomplete
    __locals_context: Incomplete
    __var_dir: Incomplete
    __evaluator: Incomplete
    __adapter: Incomplete
    __directory_name_of_pages: Incomplete
    on_action: Incomplete
    on_change: Incomplete
    on_init: Incomplete
    on_navigate: Incomplete
    on_exception: Incomplete
    on_status: Incomplete
    on_user_content: Incomplete
    __client_id_2_sid: Incomplete
    _flask_blueprint: Incomplete
    __version: Incomplete
    _markdown: Incomplete
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
    def __get_content_accessor(self): ...
    def _bindings(self): ...
    def _get_data_scope(self): ...
    def _get_config(self, name: ConfigParameter, default_value: t.Any) -> t.Any: ...
    def _get_themes(self) -> t.Optional[t.Dict[str, t.Any]]: ...
    def _bind(self, name: str, value: t.Any) -> None: ...
    def __get_state(self): ...
    def _get_client_id(self) -> str: ...
    def __set_client_id_in_context(self, client_id: t.Optional[str] = ...): ...
    def __is_var_modified_in_context(self, var_name: str, derived_vars: t.Set[str]) -> bool: ...
    def __clean_vars_on_exit(self) -> t.Optional[t.Set[str]]: ...
    def _manage_message(self, msg_type: _WsType, message: dict) -> None: ...
    def __front_end_update(
        self,
        var_name: str,
        value: t.Any,
        propagate: bool = ...,
        rel_var: t.Optional[str] = ...,
        on_change: t.Optional[str] = ...,
    ) -> None: ...
    def _update_var(
        self,
        var_name: str,
        value: t.Any,
        propagate: bool = ...,
        holder: t.Optional[_TaipyBase] = ...,
        on_change: t.Optional[str] = ...,
    ) -> None: ...
    def _get_real_var_name(self, var_name: str) -> t.Tuple[str, str]: ...
    def _call_on_change(self, var_name: str, value: t.Any, on_change: t.Optional[str] = ...): ...
    def _get_content(self, var_name: str, value: t.Any, image: bool) -> t.Any: ...
    def __serve_content(self, path: str) -> t.Any: ...
    def _get_user_content_url(
        self, path: t.Optional[str] = ..., query_args: t.Optional[t.Dict[str, str]] = ...
    ) -> t.Optional[str]: ...
    def __serve_user_content(self, path: str) -> t.Any: ...
    def __serve_extension(self, path: str) -> t.Any: ...
    def __get_version(self) -> str: ...
    def __append_libraries_to_status(self, status: t.Dict[str, t.Any]): ...
    def _serve_status(self, template: pathlib.Path) -> t.Dict[str, t.Dict[str, str]]: ...
    def __upload_files(self): ...
    def __send_var_list_update(self, modified_vars: t.List[str], front_var: t.Optional[str] = ...): ...
    def __request_data_update(self, var_name: str, payload: t.Any) -> None: ...
    def __request_var_update(self, payload: t.Any): ...
    def __send_ws(self, payload: dict) -> None: ...
    def __broadcast_ws(self, payload: dict): ...
    def __send_ack(self, ack_id: t.Optional[str]) -> None: ...
    def _send_ws_id(self, id: str) -> None: ...
    def __send_ws_download(self, content: str, name: str, on_action: str) -> None: ...
    def __send_ws_alert(self, type: str, message: str, system_notification: bool, duration: int) -> None: ...
    def __send_ws_partial(self, partial: str): ...
    def __send_ws_block(
        self,
        action: t.Optional[str] = ...,
        message: t.Optional[str] = ...,
        close: t.Optional[bool] = ...,
        cancel: t.Optional[bool] = ...,
    ): ...
    def __send_ws_navigate(self, to: str, tab: t.Optional[str]): ...
    def __send_ws_update_with_dict(self, modified_values: dict) -> None: ...
    def __send_ws_broadcast(self, var_name: str, var_value: t.Any): ...
    def __get_ws_receiver(self) -> t.Union[t.List[str], t.Any, None]: ...
    def __get_message_grouping(self): ...
    def __enter__(self): ...
    def __exit__(self, exc_type, exc_value, traceback): ...
    def __hold_messages(self) -> None: ...
    def __send_messages(self) -> None: ...
    def _get_user_function(self, func_name: str) -> t.Union[t.Callable, str]: ...
    def _get_user_instance(self, class_name: str, class_type: type) -> t.Union[object, str]: ...
    def __on_action(self, id: t.Optional[str], payload: t.Any) -> None: ...
    def __call_function_with_args(self, **kwargs): ...
    def _call_function_with_state(self, user_function: t.Callable, args: t.List[t.Any]) -> t.Any: ...
    def _call_user_callback(
        self, state_id: t.Optional[str], user_callback: t.Callable, args: t.List[t.Any], module_context: t.Optional[str]
    ) -> t.Any: ...
    def _evaluate_expr(self, expr: str) -> t.Any: ...
    def _re_evaluate_expr(self, var_name: str) -> t.Set[str]: ...
    def _refresh_expr(self, var_name: str): ...
    def _get_expr_from_hash(self, hash_val: str) -> str: ...
    def _evaluate_bind_holder(self, holder: t.Type[_TaipyBase], expr: str) -> str: ...
    def _evaluate_holders(self, expr: str) -> t.List[str]: ...
    def _is_expression(self, expr: str) -> bool: ...
    _building: Incomplete
    def _set_building(self, building: bool): ...
    def __is_building(self): ...
    def _get_rebuild_fn_name(self, name: str): ...
    def __get_attributes(self, attr_json: str, hash_json: str, args_dict: t.Dict[str, t.Any]): ...
    def _tbl_cols(
        self, rebuild: bool, rebuild_val: t.Optional[bool], attr_json: str, hash_json: str, **kwargs
    ) -> t.Union[str, _DoNotUpdate]: ...
    def _chart_conf(
        self, rebuild: bool, rebuild_val: t.Optional[bool], attr_json: str, hash_json: str, **kwargs
    ) -> t.Union[str, _DoNotUpdate]: ...
    def _add_adapter_for_type(self, type_name: str, adapter: t.Callable) -> None: ...
    def _add_type_for_var(self, var_name: str, type_name: str) -> None: ...
    def _get_adapter_for_type(self, type_name: str) -> t.Optional[t.Callable]: ...
    def _get_unique_type_adapter(self, type_name: str) -> str: ...
    def _run_adapter(
        self, adapter: t.Optional[t.Callable], value: t.Any, var_name: str, id_only: bool = ...
    ) -> t.Union[t.Tuple[str, ...], str, None]: ...
    def _get_valid_adapter_result(self, value: t.Any, id_only: bool = ...) -> t.Union[t.Tuple[str, ...], str, None]: ...
    def _is_ui_blocked(self): ...
    def __get_on_cancel_block_ui(self, callback: t.Optional[str]): ...
    def __add_pages_in_folder(self, folder_name: str, folder_path: str): ...
    def _get_locals_bind(self) -> t.Dict[str, t.Any]: ...
    def _get_default_locals_bind(self) -> t.Dict[str, t.Any]: ...
    def _get_locals_bind_from_context(self, context: t.Optional[str]) -> t.Dict[str, t.Any]: ...
    def _get_locals_context(self) -> str: ...
    def _set_locals_context(self, context: t.Optional[str]) -> None: ...
    def _reset_locals_context(self) -> None: ...
    @staticmethod
    def _get_root_page_name(): ...
    def _set_flask(self, flask: Flask): ...
    def _get_default_module_name(self): ...
    @staticmethod
    def _get_timezone() -> str: ...
    @staticmethod
    def _set_timezone(tz: str): ...
    def add_page(self, name: str, page: t.Union[str, Page], style: t.Optional[str] = ...) -> None: ...
    _root_dir: Incomplete
    def add_pages(self, pages: t.Optional[t.Union[t.Dict[str, t.Union[str, Page]], str]] = ...) -> None: ...
    def add_partial(self, page: t.Union[str, Page]) -> Partial: ...
    def _update_partial(self, partial: Partial): ...
    def _get_partial(self, route: str) -> t.Optional[Partial]: ...
    def _bind_var(self, var_name: str) -> str: ...
    def _bind_var_val(self, var_name: str, value: t.Any) -> bool: ...
    def __bind_local_func(self, name: str): ...
    def load_config(self, config: Config) -> None: ...
    def broadcast(self, name: str, value: t.Any): ...
    def _download(self, content: t.Any, name: t.Optional[str] = ..., on_action: t.Optional[str] = ...): ...
    def _notify(
        self,
        notification_type: str = ...,
        message: str = ...,
        system_notification: t.Optional[bool] = ...,
        duration: t.Optional[int] = ...,
    ): ...
    def _hold_actions(self, callback: t.Optional[t.Union[str, t.Callable]] = ..., message: t.Optional[str] = ...): ...
    def _resume_actions(self) -> None: ...
    def _navigate(self, to: t.Optional[str] = ..., tab: t.Optional[str] = ...): ...
    def __init_route(self): ...
    def _call_on_exception(self, function_name: str, exception: Exception) -> bool: ...
    def __call_on_status(self) -> t.Optional[str]: ...
    def __render_page(self, page_name: str) -> t.Any: ...
    def _render_route(self) -> t.Any: ...
    def _register_data_accessor(self, data_accessor_class: t.Type[_DataAccessor]) -> None: ...
    def get_flask_app(self) -> Flask: ...
    def _set_frame(self, frame: FrameType): ...
    def _set_state(self, state: State): ...
    def __get_client_config(self) -> t.Dict[str, t.Any]: ...
    def __get_css_vars(self) -> str: ...
    _server: Incomplete
    def __init_server(self) -> None: ...
    def __init_ngrok(self) -> None: ...
    def __bind_default_function(self) -> None: ...
    def __register_blueprint(self) -> None: ...
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
