/** @odoo-module **/

import { Component, useState } from "@odoo/owl";

export class TodoItem extends Component {
  static template = "awesome_owl.todo_item";

  markCompleted(ev) {
    this.props.toggleState(this.props.todo.id);
  }
}
