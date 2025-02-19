import { Component, useState } from "@odoo/owl";

export class TodoList extends Component {
  static template = "awesome_owl.todolist";

  setup() {
    this.todos = useState([
      { id: 1, description: "Buy Milk!!", isCompleted: false },
      { id: 2, description: "Disappear!", isCompleted: false },
    ]);
  }

  static components = {TodoItem}
}
