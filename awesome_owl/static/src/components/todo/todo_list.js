import { Component, useState } from "@odoo/owl";

export class Todo extends Component {
  static template = "awesome_owl.todo_list";
  static props = {};

  setup() {
    this.todos = useState([
      { id: 1, description: "Buy milk", isCompleted: false },
    ]);
  }
}
