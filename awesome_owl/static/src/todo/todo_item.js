/** @odoo-module **/

import { Component } from "@odoo/owl";

export class TodoItem extends Component {
  static props = {
    todo: Object,
    toggleState: Function,
    removeTodo: Function,
  };
  toggleTodo(ev) {
    this.props.toggleState(this.props.todo.id);
  }
  deleteTodo() {
    this.props.removeTodo(this.props.todo.id);
  }
}
TodoItem.template = "awesome_owl.TodoItem";
