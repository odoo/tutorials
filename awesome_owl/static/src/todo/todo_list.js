import { Component, useState } from "@odoo/owl";
import { TodoItem } from "./todo_item";
import { useAutofocus } from "../utils";

export class TodoList extends Component {
  static template = "awesome_owl.todo_list";
  static components = { TodoItem };

  setup() {
    this.todos = useState([]);
    this.newTodo = useState({ description: "" });
    useAutofocus("todoInput");
  }

  addTodo(ev) {
    if (ev.keyCode === 13 && ev.target.value) {
      this.todos.push({
        id: Date.now(),
        description: ev.target.value,
        isCompleted: false,
      });
      ev.target.value = "";
    }
  }
  toggleState(id) {
    const todo = this.todos.find((todo) => todo.id === id);
    todo.isCompleted = !todo.isCompleted;
  }

  removeTodo(id) {
    const ind = this.todos.findIndex((todo) => todo.id === id);
    if (ind >= 0) {
      this.todos.splice(ind, 1);
    }
  }
}
