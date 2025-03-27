import { Component, useState } from "@odoo/owl";

export class Card extends Component {
  static template = "awesome_owl.card";
  static props = {
    title: String,
    content: String,
    slots: {
      type: Object,
      optional: true,
      shape: {
        default: true,
      },
    },
  };
  setup() {
    this.viewCounter = useState({ value: true });
  }
  toggleCounter() {
    this.viewCounter.value = !this.viewCounter.value;
  }
}
