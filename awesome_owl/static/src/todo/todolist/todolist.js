import { Component, useState } from "@odoo/owl";
import { TodoItem } from "../todoitem/todoitem";
import { useAutofocus } from "../../utils";

export class TodoList extends Component {
  static template = "awesome_owl.todolist";

  static components = { TodoItem };

  setup() {
    ((this.todos = useState([])), (this.id = 0));
    useAutofocus("input");
  }

  add(ev) {
    if (ev.keyCode === 13 && ev.target.value != "") {
      this.todos.push({
        id: this.id++,
        description: ev.target.value,
        isCompleted: false,
      });
      ev.target.value = "";
    }
  }

  toggleTodo(todoId) {
    const todo = this.todos.find((todo) => todo.id === todoId);
    if (todo) {
      todo.isCompleted = !todo.isCompleted;
    }
  }

  removeTodoClick(todoId) {
    const index = this.todos.findIndex((todo) => todo.id === todoId);
    if (index >= 0) {
      this.todos.splice(index, 1);
    }
  }
}
