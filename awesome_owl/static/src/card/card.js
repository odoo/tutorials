import { Component, useState } from "@odoo/owl";

export class Card extends Component {
  static props = {
    title: { type: String, optional: false },
    slots: { type: Object, optional: true },
  };
  setup() {
    this.state = useState({ visibility: true });
  }

  toggleState() {
    this.state.visibility = !this.state.visibility;
  }
}

Card.template = "awesome_owl.card";
