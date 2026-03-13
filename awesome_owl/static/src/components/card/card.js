import { Component, useState } from "@odoo/owl";

export class Card extends Component {
  static template = "awesome_owl.Card";
  static props = {
    title: String,
    content: { type: String, optional: true },
    slots: { type: Object, optional: true },
  };

  setup() {
    this.toggleState = useState({ isOpen: true });
  }

  toggleAction() {
    this.toggleState.isOpen = !this.toggleState.isOpen;
  }
}
