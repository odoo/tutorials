import { Component, useState } from "@odoo/owl";

export class Card extends Component {
  static template = "awesome_owl.card";
  // defaultProps cannot be defined for non optional props
  // static defaultProps = {
  //   content: "My card content",
  // };
  static props = {
    title: String,
    // content: {
    //   type: String,
    //   optional: true,
    // },
    slots: {
      type: Object,
      shape: {
        default: true,
      },
    },
  };

  setup() {
    this.card_visibility = useState({ visible: true });
  }

  toggleVisibility = () => {
    this.card_visibility.visible = !this.card_visibility.visible;
  };
}
