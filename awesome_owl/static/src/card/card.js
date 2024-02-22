/** @odoo-module **/

import { Component, useState } from "@odoo/owl";

export class Card extends Component {
  static template = "awesome_owl.card";

  static props = {
    title: String,
    slots: Object,
  };

  setup() {
    this.state = useState({ isToggled: true });
  }

  toggleContent() {
    this.state.isToggled = !this.state.isToggled;
  }
}
