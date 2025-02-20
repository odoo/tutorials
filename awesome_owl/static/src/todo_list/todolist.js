import { Component, useState } from "@odoo/owl";
import { TodoItem } from "./todoitem";
import { useAutofocus } from "../utils";

export class TodoList extends Component {
  static template = "awesome_owl.todolist";

  setup() {
    this.todos = useState([]);
    useAutofocus("todoInput");
  }
  static components = { TodoItem };

  onKeyUpListener(event) {
    if (event.keyCode === 13 && event.target.value) {
      this.todos.push({
        id: this.todos.length + 1,
        description: event.target.value,
        isCompleted: false,
      });
      event.target.value = "";
    }
  }

  toggleTodoStatus(todoId) {
    const todo = this.todos.find((todo) => todo.id === todoId);
    todo.isCompleted = !todo.isCompleted;
  }

  removeTodo(todoId) {
    const todoIndex = this.todos.findIndex((todo) => todo.id === todoId);
    this.todos.splice(todoIndex, 1);
  }
}
