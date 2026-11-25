import { Component, useState } from "@odoo/owl";
import { TodoItem } from "./todo_item";
import { useAutofocus } from "../utils";

export class TodoList extends Component {
  static template = "awesome_owl.TodoList";
  static components = { TodoItem };

  setup() {
    this.nextId = 4;

    this.todos = useState([
      { id: 1, description: "buy milk", isCompleted: true },
      { id: 2, description: "clean room", isCompleted: true },
      { id: 3, description: "learn owl framework", isCompleted: false },
    ]);

    this.inputRef = useAutofocus("input");
  }
  addTodo(ev) {
    if (ev.key === "Enter" && ev.target.value.trim() !== "") {
      this.todos.push({
        id: this.nextId++,
        description: ev.target.value.trim(),
        isCompleted: false,
      });
      ev.target.value = "";
    }
  }

  toggleTodo(todoId) {
    const todo = this.todos.find((t) => t.id === todoId);
    if (todo) {
      todo.isCompleted = !todo.isCompleted;
    }
  }

  removeTodo(todoId) {
    const index = this.todos.findIndex((elem) => elem.id === todoId);
    if (index >= 0) {
      this.todos.splice(index, 1);
    }
  }
}
