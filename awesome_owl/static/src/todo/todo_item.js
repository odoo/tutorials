/** @odoo-module **/

import { Component, useState } from "@odoo/owl";

export class TodoItem extends Component {
  static template = "awesome_owl.todo_item";

  markCompleted() {
    this.props.toggleState(this.props.todo.id);
  }

  deleteItem() {
    this.props.removeTodo(this.props.todo.id);
  }
}
