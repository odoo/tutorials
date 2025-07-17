import { Component, useState } from "@odoo/owl";
import { TodoItem } from "./todo_item";

export class TodoList extends Component {
  static template = "awesome_owl.todo_list";
  static components = { TodoItem };
  static props = {};

  setup() {
    this.todos = useState([]);
  }

  toggleState = (id) => {
    const todo = this.todos.find((t) => t.id === id);
    if (todo) {
      todo.isCompleted = !todo.isCompleted;
    }
  };

  addTodo(ev) {
    if (ev.keyCode !== 13) return;
    const description = ev.target.value.trim();

    if (!description) return;

    this.todos.push({
      id: this.todos.length + 1,
      description: description,
      isCompleted: false,
    });

    ev.target.value = "";
  }

  onRemoveTodo = (todoId) => {
    const index = this.todos.findIndex((elem) => elem.id === todoId);
    if (index >= 0) {
      this.todos.splice(index, 1);
    }
  };
}
