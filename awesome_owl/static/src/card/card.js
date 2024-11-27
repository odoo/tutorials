import { Component, useState } from "@odoo/owl";

export class Card extends Component {
  static template = "awesome_owl.card";

  static props = {
    title: String,
    slots: { type: Object, optional: true },
  };

  setup() {
    this.state = useState({ open: true });
  }

  toggle() {
    this.state.open = !this.state.open;
  }

  static components = { Card };
}
