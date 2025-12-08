import { Component, useState } from "@odoo/owl";
import { Counter } from "../counter/counter";

export class Card extends Component {
  static template = "awesome_owl.Card";

  static components = { Counter };

  setup() {
    this.state = useState({
      open: true,
    });

    this.flip = this.flip.bind(this);
  }

  static props = {
    title: String,
  };

  flip() {
    this.state.open = !this.state.open;
  }
}
