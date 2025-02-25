import { Component, useState } from "@odoo/owl";

export class Card extends Component {
  static template = "awesome_owl.card";
  static props = {
    title: {
      type: String,
      // default wont work when optional is not set
      default: "My Title",
    },
    content: {
      type: String,
      optional: true,
      default: "my card content",
    },
  };

  /*
  use of state is not needed here as we are passing static values inside props, this can be used where values are inserted by user with onchange attribute
  */

  // setup() {
  //   this.state = useState({
  //     title: this.props.title,
  //     content: this.props.content,
  //   });
  // }
}
