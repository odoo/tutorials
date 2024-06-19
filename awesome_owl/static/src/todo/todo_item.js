/** @odoo-module **/

import { Component } from "@odoo/owl";

export class TodoItem extends Component {
  static props = {
    todo: {
      type: Object,
      shape: {
        id: Number,
        description: String,
        isCompleted: Boolean,
      },
    },
    toggleCompleted: Function,
    removeTodo: Function,
  };
  static template = "awesome_owl.todo_item";

  onCheckboxChange() {
    this.props.toggleCompleted(this.props.todo.id);
  }

  onDelete() {
    this.props.removeTodo(this.props.todo.id);
  }
}
