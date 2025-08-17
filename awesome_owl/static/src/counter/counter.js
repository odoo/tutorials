import { Component, useState, onMounted } from "@odoo/owl";

export class Counter extends Component {
  static template = "awesome_owl.Counter";
  static props = {
    value: {
      type: Number,
      optional: true,
    },
    onChange: {
      type: Function,
      optional: true,
    },
    onLoad: {
      type: Function,
      optional: true,
    },
  };

  setup() {
    // extra : tried passing props value from parent without validation
    // using ternary operator is the wrong way of passing default value, use defaultProps for this
    this.state = useState({ value: this.props.value ? this.props.value : 0 });

    // extra : takes props (value) from parent while calling component as initial value of sum
    onMounted(() => {
      if (this.props.onLoad) {
        this.props.onLoad(this.state.value);
      }
    });
  }

  increment() {
    this.state.value++;
    if (this.props.onChange) {
      this.props.onChange();
    }
  }
}
