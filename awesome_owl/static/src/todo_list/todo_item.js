/** @odoo-module **/

import { Component, useRef, onMounted } from "@odoo/owl";

export class TodoItem extends Component {
  static template = "awesome_owl.TodoItem";
  static props = {
    todo: {
      id: Number,
      description: String,
      isCompleted: Boolean,
    },
    toggleState: { Function },
    removeTodo: { Function },
  };

  onClickToggleState() {
    this.props.toggleState(this.props.todo.id);
  }

  onClickRemoveTodo() {
    this.props.removeTodo(this.props.todo.id);
  }
}
