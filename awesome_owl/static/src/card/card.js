import { Component, useState } from "@odoo/owl";

export class Card extends Component {
  static template = "awesome_owl.Card";

  setup() {
    this.state = useState({ value: true });
  }

  toggleState() {
    this.state.value = !this.state.value;
  }

  static props = {
    name: String,
    slots: {
      type: Object,
      optional: true,
    },
  };
}
