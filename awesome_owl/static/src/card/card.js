/** @odoo-module **/

import { Component, useState } from "@odoo/owl";

export class Card extends Component {
  static props = {
    title: String,
    slots: {
      type: Object,
      shape: {
        default: Object,
      },
    },
  };
  static template = "awesome_owl.card";

  setup() {
    this.state = useState({ isOpen: true });
  }

  toggleOpen() {
    this.state.isOpen = !this.state.isOpen;
  }
}
