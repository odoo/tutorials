/** @odoo-module **/

import { Component, useState } from "@odoo/owl";
import { TodoItem } from "./todo_item";
import { useAutofocus } from "../utils";

export class TodoList extends Component {
  static template = "awesome_owl.TodoList";
  static components = { TodoItem };

  setup() {
    this.todos = useState([]);
    useAutofocus("input");
  }

  addTodo(ev) {
    const desc = ev.target.value;
    if (ev.keyCode === 13 && desc != "") {
      this.todos.push({
        id: (this.todos.findLast(() => true)?.id + 1) | 0,
        description: desc,
        isCompleted: false,
      });

      ev.target.value = "";
    }
  }

  toggleState(id) {
    const todo = this.todos.find((x) => x.id == id);
    todo.isCompleted = !todo.isCompleted;
  }

  removeTodo(id) {
    const index = this.todos.findIndex((x) => x.id == id);

    if (index >= 0) this.todos.splice(index, 1);
  }
}
