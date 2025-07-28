import { Component } from "@odoo/owl";

export class Card extends Component {
  static template = "awesome_owl.card";

  static defaultProps = {
    title: "Default Title",
  };

  static props = {
    title: {
      type: String,
      optional: true,
    },
    content: { type: String },
  };
}
