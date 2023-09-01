/** @odoo-module **/

import { Component, useState } from "@odoo/owl";
import { Todo } from "../Todo/todo";
import { useAutofocus } from "../utils";
export class TodoList extends Component {
  static template = "owl_playground.Todo-List";
  setup() {
    this.state = useState({ todoList: [] });
    this.counter = 1;
    useAutofocus("AddTaskInput");
  }
  addTodo(event) {
    if (event.keyCode === 13 && event.target.value !== "") {
      this.state.todoList.push({
        id: this.counter++,
        description: event.target.value,
        done: false,
      });
      event.target.value = "";
    }
  }
  toggleTodo(todoId) {
    const todo = this.state.todoList.find((todo) => todo.id === todoId);
    if (todo) {
      todo.done = !todo.done;
    }
  }

  removeTodo(todoId) {
    const todoIndex = this.state.todoList.findIndex(
      (todo) => todo.id === todoId
    );

    if (todoIndex !== -1) {
      this.state.todoList.splice(todoIndex, 1);
    }
  }
  static components = { Todo };
}
