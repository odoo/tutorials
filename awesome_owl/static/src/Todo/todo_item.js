import { Component, useState } from "@odoo/owl";

export class TodoItem extends Component {
  static template = "awesome_owl.TodoItem";
  static props = {
    todo: {
      type: Object,
      shape: { id: Number, description: String, isCompleted: Boolean },
    },
    toggleState: {
      type: Function,
    },
    deleteTodo: {
      type: Function,
    },
  };

  onChange() {
    this.props.toggleState(this.props.todo);
  }

  onClick() {
    this.props.deleteTodo(this.props.todo.id);
  }
}
