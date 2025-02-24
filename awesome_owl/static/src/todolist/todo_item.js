/** @odoo-module */

import { Component } from "@odoo/owl";

export class TodoItem extends Component {
  static template = "awesome_owl.todo_item";
  static props = {
    todo: { id: Number, description: String, isCompleted: Boolean },
    toggleState: { type: Function },
    removeTodo: { type: Function },
  };

  toggleCompleted() {
    this.props.toggleState(this.props.todo.id);
  }

  deleteTodo() {
    this.props.removeTodo(this.props.todo.id);
  }
}