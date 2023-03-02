// Implementation of the React component "ColoredLabel".
//
// This component displays a text string changing the color of
// each successive letter.
import React from "react";
import { useDynamicProperty } from "taipy-gui";

interface ColoredLabelProps {
  value?: string;
  defaultValue?: string;
}

// Sequence of colors
const colorWheel = ["#FF0000", "#A0A000", "#00FF00", "#00A0A0", "#0000FF", "#A000A0"]
// Return the color style depending on the character index
const getColor = (index: number) => ({ color: colorWheel[index % 6] });

// ColoredLabel component definition
const ColoredLabel = (props: ColoredLabelProps) => {
  // The dynamic property that holds the text value
  const value = useDynamicProperty(props.value, props.defaultValue, "");
  // Empty text?
  if (!value) {
    return <span />
  }
  // Create a <span> element for each letter with the proper style.
  // Note that React needs, in this situation, to set the 'key' property
  // with a unique value for each <span> element.
  return (
    <>
      {value.split("").map((letter, index) => (
        <span key={"key" + index} style={getColor(index)}>{letter}</span>
      ))}
    </>
  )
}

export default ColoredLabel;
