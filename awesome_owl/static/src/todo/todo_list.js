/** @odoo-module **/

import { Component, useRef, useState } from "@odoo/owl";
import { TodoItem } from "./todo_item";
import { useAutofocus } from "../utils";

export class TodoList extends Component {
  static props = [];
  static template = "awesome_owl.todo_list";
  static components = { TodoItem };

  setup() {
    this.todos = useState([]);
    this.inputRef = useRef("input");
    useAutofocus(this.inputRef);
  }

  addTodo(event) {
    if (event.key !== "Enter" || !event.target.value) {
      return;
    }

    const currentIds = this.todos.map((todo) => todo.id);
    const newId = currentIds.length > 0 ? Math.max(...currentIds) + 1 : 1;

    const newTodo = {
      id: newId,
      description: event.target.value,
      isCompleted: false,
    };

    this.todos.push(newTodo);
  }

  toggleCompleted(todoId) {
    const todo = this.todos.find((todo) => todo.id === todoId);
    if (todo) {
      todo.isCompleted = !todo.isCompleted;
    }
  }

  removeTodo(todoId) {
    const todoIndex = this.todos.findIndex((todo) => todo.id === todoId);
    if (todoIndex >= 0) {
      this.todos.splice(todoIndex, 1);
    }
  }
}
