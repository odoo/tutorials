import { Component, useState } from "@odoo/owl";

export class Card extends Component {
  static template = "awesome_owl.card";
  setup() {
    this.state = useState({
      toggleview: true,
    });
  }
  static props = {
    title: {
      type: String,
    },
    slots: {
      type: Object,
    },
  };
  toggleCard() {
    this.state.toggleview = !this.state.toggleview;
    // console.log("this.state.toggleview")
  }
}
