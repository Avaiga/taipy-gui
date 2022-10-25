# Taipy visual elements documentation

Taipy visual elements are React components that are created after they were defined from Python code.

What is exposed to the programmer is the set of properties that each visual element understands. This
directory contains all it needs to generate the functional documentation for Taipy programmers to use.

For every visual component, you need to provide or update two files:

   - `<element_name>.md`: A free Markdown text introduction to the element, and a list of usage examples.
     The generated reference part for this element type's documentation is inserted just before
     the first occurence of "##" (level 2 title).

   - `viselements.json`: the list of all visual element descriptors.

     An element descriptor indicates all that needs to be exposed for user, in the
     documentation or in Taipy Studio.
  
     Element descriptors appear in one of three lists: "controls", "blocks" or "others". The order
     of the elements in the "controls" and "blocks" list is the one reflected in the documentation.

     Element descriptors *may* hold the following properties:

     - "default": the name of the default property for the described element.

     - "inherits": if the element inherits some property interfaces (like "shared"), you must
       add those interface names to the property value (like ["shared"]).

       All the properties of the interface will be listed as properties of the visual element.

       If you need to have an inherited property appearing elsewhere in the property list,
       simply indicate its name filling the other properties if needed.

     Element descriptors *must* have the "properties" property that  holds the list of its properties,
     in the order you want them to appear in the visual element documentation page.

     The following rules apply to the different properties for the element properties:

     - "name": the name of the property.

       If the property is the default property, this property value must be reflected
       in the "default" property.

     - "type": the type of this property.

       If the property accepts several types, you can separate the type names with a
       vertical bar (|) character.

       If the type is a dictionary, make sure you indicate the expected types
       for both the key and value.

       If the property is dynamic, it should be reflected by surrounding the type
       (or sequence of type names) by `dynamic(...)`.
       
       You cannot use any Markdown in this property value. You must use raw HTML.

     - "default": the default value for this property.

       If there is no default value, set this to null (or just drop the property itself).

     - "doc": The actual documentation for this property.

       You cannot use any Markdown in this property value. You must use raw HTML.
