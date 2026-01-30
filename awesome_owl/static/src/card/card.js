/** @odoo-module **/
import { Component , useState } from "@odoo/owl";

export class Card extends Component {
    static template = "awesome_owl.Card";
    static props = {
        title: { type: String },
        slots: { type: Object, optional: true },
        content: { type: String, optional: true },
    };
    setup() {
    this.state = useState({ open: true });
  }

  toggle() {
    this.state.open = !this.state.open;
  }

}
