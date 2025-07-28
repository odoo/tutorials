import { Component, useState } from "@odoo/owl";

export class Card extends Component {
  static template = "awesome_owl.card";

  static defaultProps = {
    title: "Default Title",
  };

  setup() {
    this.state = useState({ isOpen: true });
  }

  toggleContent() {
    this.state.isOpen = !this.state.isOpen;
  }

  static props = {
    title: {
      type: String,
      optional: true,
    },
    "*": true,
  };
}
