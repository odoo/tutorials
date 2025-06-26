/** @odoo-module **/

import { Component } from "@odoo/owl";

export class TodoItem extends Component {
  static template = "awesome_owl.TodoItem";

  static props = {
    todo: {
      type: Object,
      shape: {
        id: Number,
        description: String,
        isCompleted: Boolean,
      },
      optional: false,
    },
    toggleState: { type: Function, optional: false },
    removeTodo: { type: Function, optional: false },
  };

  onCheckboxChange() {
    this.props.toggleState(this.props.todo.id);
  }

  onDeleteClick() {
    this.props.removeTodo(this.props.todo.id);
  }

  toggleCompletion() {
    const newTodo = {
      ...this.props.todo,
      isCompleted: !this.props.todo.isCompleted,
    };
    this.props.onChange(newTodo);
  }
}
