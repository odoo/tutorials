/** @odoo-module **/
import { Component, useState } from "@odoo/owl";
import { TodoItem } from "./todo_item";

export class TodoList extends Component {
  static template = "awesome_owl.todo_list";
  static components = { TodoItem };

  setup() {
    this.todos = useState([
      { id: 3, description: "buy milk", isCompleted: false },
    ]);
  }
}
