/** @odoo-module **/

import { Component, useState } from "@odoo/owl";

export class Card extends Component {
  static template = "awesome_owl.card";

  // Props validation
  static props = {
    title: { type: String, optional: false },
    slots: {
      type: Object,
      shape: { default: true },
    },
  };

  setup() {
    // Track whether the card content is visible or collapsed
    this.state = useState({ isOpen: true });
  }

  // Toggle open/close state
  toggleOpen() {
    this.state.isOpen = !this.state.isOpen;
  }

}
