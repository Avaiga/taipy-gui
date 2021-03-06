A control that can trigger a function when pressed.

## Usage

### Simple text

The button label, which is the button control's default property, is simply displayed as the button
text.

!!! example "Page content"

    === "Markdown"

        ```
        <|Button Label|button|>
        ```
  
    === "HTML"

        ```html
        <taipy:button>Button Label</taipy:button>
        ```

### Specific action callback

Button can specify a callback function to be invoked when the button is pressed.

!!! example "Page content"

    === "Markdown"

        ```
        <|Button Label|button|on_action=button_action_function_name|>
        ```

    === "HTML"

        ```html
        <taipy:button on_action="button_action_function_name">Button Label</taipy:button>
        ```

