import { Component, useState } from "@odoo/owl";
import { TodoItem } from "./todo_item";
import { useAutofocus } from "../utils";

export class TodoList extends Component {
  static template = "awesome_owl.TodoList";
  static components = { TodoItem };
  static props = {};
  setup() {
    this.ids = 1;
    this.todos = useState([]);
    useAutofocus("input");
  }

  addTodo(ev) {
    if (ev.keyCode === 13 && ev.target.value != "") {
      let desc = ev.target.value;

      this.todos.push({
        id: this.ids++,
        description: desc,
        isCompleted: false,
      });
      ev.target.value = "";
    }
  }

  toggleTodoComplete(element) {
    const todoElement = this.todos.find((todo) => element.id == todo.id);
    if (todoElement) {
      todoElement.isCompleted = !todoElement.isCompleted;
    }
  }

  removeTodo = (element_id) => {
    const todoElement = this.todos.findIndex((todo) => todo.id == element_id);
    if (todoElement >= 0) {
      this.todos.splice(todoElement, 1);
    }
  };
}
