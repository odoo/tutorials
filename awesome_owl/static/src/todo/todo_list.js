/** @odoo-module **/

import { Component, useState } from "@odoo/owl";
import { TodoItem } from "./todo_item.js";

let nextId = 0;
export class TodoList extends Component {
  static template = "awesome_owl.TodoList";
  static components = { TodoItem };

  setup() {
    this.todos = useState([]);
    this.inputRef = useState({ value: "" });
  }

  toggleState = (id) => {
    const todo = this.todos.find((t) => t.id === id);
    if (todo) {
      todo.isCompleted = !todo.isCompleted;
    }
  };
  removeTodo = (id) => {
    const index = this.todos.findIndex((t) => t.id === id);
    if (index >= 0) {
      this.todos.splice(index, 1);
    }
  };
  addTodo(ev) {
    if (ev.keyCode === 13) {
      const desc = this.inputRef.value.trim();
      if (!desc) return;

      this.todos.push({
        id: nextId++,
        description: desc,
        isCompleted: false,
      });

      this.inputRef.value = "";
    }
  }
}
