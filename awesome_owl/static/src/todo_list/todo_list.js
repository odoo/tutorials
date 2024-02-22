/** @odoo-module **/

import { Component, useState } from "@odoo/owl";
import { TodoItem } from "./todo_item";

export class TodoList extends Component {
  static template = "awesome_owl.todoList";
  static components = { TodoItem };

  setup() {
    this.todos = useState([]);
  }

  addTodo(e) {
    if (e.keyCode === 13 && e.target.value !== "") {
      this.todos.push({
        id: this.todos.length + 1,
        description: e.target.value,
        isCompleted: false,
      });
      e.target.value = "";
    }
  }
}
