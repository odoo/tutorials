/** @odoo-module **/

import { Component, useState } from "@odoo/owl";

export class Card extends Component {
  static template = "awesome_owl.Card";

  static props = {
    title: { type: String },
    slots: { type: Object, optional: true },
  };

  setup() {
    this.state = useState({ isOpen: true });
  }

  onClickToggle() {
    this.state.isOpen = !this.state.isOpen;
  }
}
