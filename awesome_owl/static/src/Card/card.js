/** @odoo-module */

import { Component, useState } from "@odoo/owl";

export class Card extends Component {
  static template = "awesome_owl.Card";
  static props = {
    title: { type: String, optional: true },
    slots: {},
  };
  setup() {
    this.state = useState({ isOpen: true });
  }
  toggle() {
    this.state.isOpen = !this.state.isOpen;
  }
}
