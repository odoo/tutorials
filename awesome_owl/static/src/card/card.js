import { Component, useState } from "@odoo/owl";

export class Card extends Component {
    static template = "awesome_owl.card";

    static props = {
        title: String,
        slots: Object
      };

    state = useState({ open: true });

    flipState() {
      this.state.open = !this.state.open;
  }
}