import React from "react";
import { useDynamicProperty } from "taipy-gui";

interface LabelProps {
  value?: string;
  defaultValue?: string;
}

const Label = (props: LabelProps) => {
  const value = useDynamicProperty(props.value, props.defaultValue, "");
  return <span>* {value} *</span>
}

// Note that for this very simple component, we could have used a one-liner:
// const Label = (props: LabelProps) => <span>Custom Label: {useDynamicProperty(props.value, props.defaultValue, "")}</span>

export default Label;
