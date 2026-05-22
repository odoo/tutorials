import { Component, useState } from "@odoo/owl";

export class Card extends Component {
  static template = "awesome_owl.Card";

  setup() {
    this.state = useState({ minimized: false });
    this.toggle = this.toggle.bind(this);
  }

  toggle() {
    console.log("toggle");
    console.log(this.state.minimized);
    this.state.minimized = !this.state.minimized;
    console.log(this.state.minimized);
  }
}
