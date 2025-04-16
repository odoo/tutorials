import { Component, useState } from "@odoo/owl";

export class Card extends Component {
  static template = "awesome_owl.card";

  static props = {
    title: { type: String, optional: false },
    slots: { type: Object, optional: true },
  };

  setup() {
    this.state = useState({
      isOpen: true,  // default: content is visible
    });
  }

  toggleOpen() {
    this.state.isOpen = !this.state.isOpen;
  }
}
