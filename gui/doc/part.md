Displays its children in a block.

The `part` control is used to group controls in a single element. 
This allows to show or hide them in one action and be placed as a unique element in a [`Layout`](layout.md) cell.

There is a simplified Markdown syntax to create a `part`, where the element name is optional:

`<|` just before the end of the line indicates the beginning of a `part` element;
`|>` at the beginning of a line indicated the end of the `part` definition.

## Usage

### Grouping controls

!!! example "Page content"

    === "Markdown"

        ```
        <|
            ...
            <|{Some Content}|>
            ...
        |>
        ```
  
    === "HTML"

        ```html
        <taipy:part>
            ...
            <taipy:text>{Some Content}</taipy:text>
            ...
        </taipy:part>
        ```

### Showing and hiding controls

!!! example "Page content"

    === "Markdown"

        ```
        <|part|don't render|
            ...
            <|{Some Content}|>
            ...
        |>
        ```
  
    === "HTML"

        ```html
        <taipy:part render="False">
            ...
            <taipy:text>{Some Content}</taipy:text>
            ...
        </taipy:part>
        ```

If the _render_ property is bound to a Boolean value, the `part` will show or hide its elements according to the value of the bound variable.

### Part with page

The content of the part can be specified as an existing page name using the _page_ property.

!!! example "Page content"

    === "Markdown"

        ```
        <|part|page=page_name|>
        ```
  
    === "HTML"

        ```html
        <taipy:part page="page_name"/>
        ```

### Part with partial

The content of the part can be specified as a `Partial^` instance using the _partial_ property.

!!! example "Page content"

    === "Markdown"

        ```
        <|part|partial={partial}|>
        ```
  
    === "HTML"

        ```html
        <taipy:part partial="{partial}" />
        ```
