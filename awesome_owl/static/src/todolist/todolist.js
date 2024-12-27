import { Component, useState } from "@odoo/owl";
import { Todo } from "./todo";

export class TodoList extends Component {
  static template = "awesome_owl.todolist";
  static props = {};
  static components = { Todo };

  setup() {
    this.state = useState({
      todos: [
        { id: 0, description: "buy milk", isCompleted: false },
        { id: 1, description: "drink water", isCompleted: false },
        { id: 2, description: "play soccer", isCompleted: true },
      ],
    });
  }

  addTodo(event) {
    if (event.keyCode == 13 && event.target.value != "") {
      this.state.todos.push({
        id: this.state.todos.length,
        description: event.target.value,
        isCompleted: false,
      });
      event.target.value = "";
      console.log(this.state.todos);
    }
  }
}
