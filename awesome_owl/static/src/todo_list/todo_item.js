import { Component, useState } from "@odoo/owl";

export class TodoItem extends Component {
  static template = "awesome_owl.TodoItem";
  static props = {
    todo: {
      type: Object,
      shape: { id: Number, description: String, isCompleted: Boolean },
    },
    removeTodo: Function,
  };

  delete() {
    this.props.removeTodo(this.props.todo.id);
  }

  toggleState(ev) {
    this.props.todo.isCompleted = !this.props.todo.isCompleted;
  }
}
