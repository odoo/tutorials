import { Component, useState } from "@odoo/owl";
import { TodoItem } from "./todo-item";
import { useAutofocus } from "../utils";

export class TodoList extends Component {
  static template = "awesome_owl.TodoList";

  static components = { TodoItem };

  setup() {
    this.todos = useState([]);
    this.nextId = 1;
    this.inputRef = useAutofocus("todoInput");
  }

  addTodo(event) {
    if (event.key === "Enter" && event.target.value.trim()) {
      const newTodo = {
        id: this.nextId++,
        description: event.target.value.trim(),
        isCompleted: false,
      };
      this.todos.push(newTodo);
      event.target.value = "";
      this.inputRef.el.focus();
    }
  }

  toggleState(todoId) {
    const todo = this.todos.find((t) => t.id === todoId);
    if (todo) {
      todo.isCompleted = !todo.isCompleted;
    }
  }

  deleteTodo(todoId) {
    const index = this.todos.findIndex((todo) => todo.id === todoId);
    if (index !== -1) {
      this.todos.splice(index, 1);
    }
  }
}
