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
