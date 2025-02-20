import { Component, useState } from "@odoo/owl";

export class Card extends Component {
  static template = "awesome_owl.card";

  static props = {
    title: { type: String, optional: true },
    slots: {
      type: Object,
      optional: true,
    },
  };

  setup() {
    this.state = useState({
      isCounterOpen: false,
    });
  }

  toggleCounter() {
    this.state.isCounterOpen = !this.state.isCounterOpen;
  }
}
