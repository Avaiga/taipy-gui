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

import threading
import typing as t
import warnings

from .gui import Gui
from .state import State


def download(state: State, content: t.Any, name: t.Optional[str] = "", on_action: t.Optional[str] = ""):
    """Download content to the client.

    Arguments:
        state (State^): The current user state as received in any callback.
        content: File path or file content.
        name: File name for the content on the client browser (default to content name).
        on_action: Function called when the download starts.
    """
    if state and isinstance(state._gui, Gui):
        state._gui._download(content, name, on_action)
    else:
        warnings.warn("'download()' must be called in the context of a callback")


def notify(
    state: State,
    notification_type: str = "I",
    message: str = "",
    system_notification: t.Optional[bool] = None,
    duration: t.Optional[int] = None,
):
    """Send a notification to the user interface.

    Arguments:
        state (State^): The current user state as received in any callback.
        notification_type: The notification type. This can be one of _"success"_, _"info"_,
            _"warning"_, or _"error"_.<br/>
            To remove the last notification, set this parameter to the empty string.
        message: The text message to display.
        system_notification: If True, the system will also show the notification.
            If not specified or set to None, this parameter will use the value of
            _configuration[system_notification]_.
        duration: The time, in milliseconds, during which the notification is shown.
            If not specified or set to None, this parameter will use the value of
            _configuration[notification_duration]_.

    Note that you can also call this function with _notification_type_ set to the first letter
    or the alert type (ie setting _notification_type_ to "i" is equivalent to setting it to
    "info").

    If _system_notification_ is set to True, then the browser requests the system
    to display a notification as well. They usually appear in small windows that
    fly out of the system tray.<br/>
    The first time your browser is requested to show such a system notification for
    Taipy applications, you may be prompted to authorize the browser to do so. Please
    refer to your browser documentation for details on how to allow or prevent this
    feature.
    """
    if state and isinstance(state._gui, Gui):
        state._gui._notify(notification_type, message, system_notification, duration)
    else:
        warnings.warn("'notify()' must be called in the context of a callback")


def hold_control(
    state: State,
    callback: t.Optional[t.Union[str, t.Callable]] = None,
    message: t.Optional[str] = "Work in Progress...",
):
    """Hold the User Interface actions.

    When the User Interface is held, users cannot interact with visual elements.<br/>
    The application must call `resume_control()^` so that users can interact again
    with the visual elements.

    Arguments:
        state (State^): The current user state as received in any callback.
        callback (Optional[Union[str, Callable]]): the function to be called if the user
            chooses to cancel.<br/>
            If empty or None, no cancel action is provided to the user.
        message: the message to show.
    """
    if state and isinstance(state._gui, Gui):
        state._gui._hold_actions(callback, message)
    else:
        warnings.warn("'hold_actions()' must be called in the context of a callback")


def resume_control(state: State):
    """Resume the User Interface actions.

    This function must be called after `hold_control()^` was invoked, when interaction
    must be allowed again for the user.

    Arguments:
        state (State^): The current user state as received in any callback.
    """
    if state and isinstance(state._gui, Gui):
        state._gui._resume_actions()
    else:
        warnings.warn("'resume_actions()' must be called in the context of a callback")


def navigate(state: State, to: t.Optional[str] = ""):
    """Navigate to a page.

    Arguments:
        state (State^): The current user state as received in any callback.
        to: The name of the page to navigate to. This must be a valid page identifier.
            If ommitted, the application navigates to the root page.
    """
    if state and isinstance(state._gui, Gui):
        state._gui._navigate(to)
    else:
        warnings.warn("'navigate()' must be called in the context of a callback")


def get_state_id(state: State) -> t.Optional[str]:
    """Get the identifier of a state.

    The state identifier is a string generated by Taipy GUI for a given `State^` that is used
    to serialize callbacks.
    See the [User Manual section on Long Running Callbacks](../../gui/callbacks/#long-running-callbacks)
    for details on when and how this function can be used.

    Arguments:
        state (State^): The current user state as received in any callback.

    Returns:
        A string that uniquely identifies the state.<br/>
        If None, then **state** was not handled by a `Gui^` instance.
    """
    if state and isinstance(state._gui, Gui):
        return state._gui._get_client_id()
    return None


def get_context_id(state: State) -> t.Any:
    warnings.warn("'get_context_id()' was deprecated in Taipy GUI 2.0. Use 'get_state_id()' instead.")
    return get_state_id(state)


def get_module_name_from_state(state: State) -> t.Optional[str]:
    """Get the module name that triggered a callback.

    Pages can be defined in different modules yet share callbacks declared elsewhere (typically, the
    application's main module).

    This function returns the name of the module where the page that holds the control that
    triggered the callback was declared.  This lets applications implement different behaviors
    depending on what page is involved.

    This function must be called only in the body of a callback function.

    Arguments:
        state (State^): The `State^` instance, as received in any callback.

    Returns:
        The name of the module that holds the definition of the page containing the control
            that triggered the callback that was provided the *state* object.
    """
    if state and isinstance(state._gui, Gui):
        return state._gui._get_locals_context()
    return None


def invoke_callback(gui: Gui, state_id: str, callback: t.Callable, args: t.Union[t.Tuple, t.List]) -> t.Any:
    """Invoke a user callback in a given state.

    See the [User Manual section on Long Running Callbacks in a Thread](../../gui/callbacks/#long-running-callbacks-in-a-thread)
    for details on when and how this function can be used.

    Arguments:
        gui (Gui^): The current gui instance.
        state_id: The identifier of the state to use, as returned by `get_state_id()^`.
        callback (Callable[[State^, ...], None]): The user-defined function that is invoked.<br/>
            The first parameter of this function **must** be a `State^`.
        args (Union[Tuple, List]): The remaining arguments, as a List or a Tuple.
    """
    if isinstance(gui, Gui):
        return gui._call_user_callback(state_id, callback, list(args))
    warnings.warn("'invoke_callback()' must be called with a valid Gui instance")


def invoke_state_callback(gui: Gui, state_id: str, callback: t.Callable, args: t.Union[t.Tuple, t.List]) -> t.Any:
    warnings.warn("'invoke_state_callback()' was deprecated in Taipy GUI 2.0. Use 'invoke_callback()' instead.")
    return invoke_callback(gui, state_id, callback, args)


def invoke_long_callback(
    state: State,
    user_function: t.Callable,
    user_function_args: t.Union[t.Tuple, t.List] = [],
    user_status_function: t.Optional[t.Callable] = None,
    user_status_function_args: t.Union[t.Tuple, t.List] = [],
    period=0,
):
    """Invoke a long running user callback.

    Long-running callbacks are run in a separate thread to not block the application itself.

    This function expects to be provided a function to run in the background (in *user_function*).<br/>
    It can also be specified a *status function* that is called when the operation performed by
    *user_function* is finished (successfully or not), or periodically (using the *period* parameter).

    See the [User Manual section on Long Running Callbacks](../../gui/callbacks/#long-running-callbacks)
    for details on when and how this function can be used.

    Arguments:
        state (State^): The `State^` instance, as received in any callback.
        user_function (Callable[[...], None]): The function that will be run independently of Taipy GUI. Note
            that this function must not use *state*, which is not persisted across threads.
        user_function_args (Optional[List|Tuple]): The arguments to send to *user_function*.
        user_status_function (Optional(Callable[[State^, bool, ...], None])): The optional user-defined status
            function that is invoked at the end of and possibly during the runtime of *user_function*:

            - The first parameter of this function is set to a `State^` instance.
            - The second parameter of this function is set to a bool or an int, depending on the
              conditions under which it is called:

               - If this parameter is set to a bool value, then:

                   - If True, this indicates that *user_function* has finished properly.
                   - If False, this indicates that *user_function* failed.

               - If this parameter is set to an int value, then this value indicates
                 how many periods (as lengthy as indicated in *period*) have elapsed since *user_function* was
                 started.
        user_status_function_args (Optional[List|Tuple]): The remaining arguments of the user status function.
        period (int): The interval, in milliseconds, at which *user_status_function* is called.<br/>
            The default value is 0, meaning no call to *user_status_function* will happen until *user_function*
            terminates (then the second parameter of that call will be ).</br>
            When set to a value smaller than 500, *user_status_function* is called only when *user_function*
            terminates (as if *period* was set to 0).
    """
    if not state or not isinstance(state._gui, Gui):
        warnings.warn("'invoke_long_callback()' must be called in the context of a callback.")
        return

    state_id = get_state_id(state)
    if not isinstance(state_id, str):
        return

    this_gui = state._gui

    def callback_on_exception(state: State, function_name: str, e: Exception):
        if not this_gui._call_on_exception(function_name, e):
            warnings.warn(f"invoke_long_callback: Exception raised in function {function_name}.\n{e}")

    def callback_on_status(
        status: t.Union[int, bool], e: t.Optional[Exception] = None, function_name: t.Optional[str] = None
    ):
        if callable(user_status_function):
            invoke_callback(this_gui, str(state_id), user_status_function, [status] + list(user_status_function_args))
        if e:
            invoke_callback(
                this_gui,
                str(state_id),
                callback_on_exception,
                (
                    str(function_name),
                    e,
                ),
            )

    def user_function_in_thread(*uf_args):
        try:
            user_function(*uf_args)
            callback_on_status(True)
        except Exception as e:
            callback_on_status(False, e, user_function.__name__)

    def thread_status(name: str, period_s: float, count: int):
        active_thread = next((t for t in threading.enumerate() if t.name == name), None)
        if active_thread:
            callback_on_status(count)
            threading.Timer(period_s, thread_status, (name, period_s, count + 1)).start()

    thread = threading.Thread(target=user_function_in_thread, args=user_function_args)
    thread.start()
    if isinstance(period, int) and period >= 500 and callable(user_status_function):
        thread_status(thread.name, period / 1000.0, 0)
