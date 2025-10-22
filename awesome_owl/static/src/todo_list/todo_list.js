import { Component, useState } from "@odoo/owl";
import { useAutofocus } from "../utils";
import { TodoItem } from "./todo_item";

export class TodoList extends Component {
  static template = "awesome_owl.TodoList";
  static components = { TodoItem };
  static props = [];

  setup() {
    this.todos = useState([]);
    this.index = 0;
    useAutofocus("input");
  }

  addTodo(ev) {
    if (ev.keyCode === 13 && ev.target.value != "") {
      this.todos.push({
        id: this.index++,
        description: ev.target.value,
        isCompleted: false,
      });
      ev.target.value = "";
    }
  }

  removeTodo(elemId) {
    const index = this.todos.findIndex((elem) => elem.id === elemId);
    if (index !== -1) {
      this.todos.splice(index, 1);
    }
  }
}
