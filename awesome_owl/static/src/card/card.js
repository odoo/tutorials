/** @odoo-module **/

import { Component, useState } from "@odoo/owl";

export class Card extends Component {
  static template = "awesome_owl.card";

  setup() {
    this.state = useState({ open: true });
  }

  static props = {
    title: String,
    slots: { type: Object, optional: true },
  };

  toggleOpen() {
    this.state.open = !this.state.open;
  }
}
