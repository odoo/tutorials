import { Component } from "@odoo/owl";

export class TodoItems extends Component {
  static template = "awesome_owl.todoitems";
  static props = {
    todo: {
      type: Object,
      shape: { id: Number, description: String, isComplete: Boolean },
    },
    onClick: { type: Function },
    onRemove: { type: Function },
  };

  onClick() {
    if (this.props.onClick) {
      this.props.onClick();
    }
  }

  onRemove() {
    if (this.props.onClick) {
      this.props.onRemove();
    }
  }
}

