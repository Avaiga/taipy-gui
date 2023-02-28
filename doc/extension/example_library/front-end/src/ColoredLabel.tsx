import React from "react";
import { useDynamicProperty } from "taipy-gui";

interface ColoredLabelProps {
  value?: string;
  defaultValue?: string;
}

const colorWheel = ["#FF0000", "#A0A000", "#00FF00", "#00A0A0", "#0000FF", "#A000A0"]

const ColoredLabel = (props: ColoredLabelProps) => {
  const value = useDynamicProperty(props.value, props.defaultValue, "");
  if (!value) {
    return <span />
  }
  const getColor = (index: number) => ({ color: colorWheel[index % 6] });
  return value.split('').map((letter, index) =>
    <span style={getColor(index)} >{letter}</span>
  )
}

  // Note that for this very simple component, we could have used a one-liner:
// const Label = (props: LabelProps) => <span>Custom Label: {useDynamicProperty(props.value, props.defaultValue, "")}</span>

export default ColoredLabel;
