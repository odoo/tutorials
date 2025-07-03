import { Component, useState } from "@odoo/owl";
import { TodoItem } from "./todoItem";
import { useAutofocus } from "../utils/utils";
export class TodoList extends Component {
  static template = "awesome_owl.TodoList";
  static components = { TodoItem };

  setup() {
    this.todos = useState([
      { id: 1, description: "buy milk", isCompleted: false },
      { id: 2, description: "write tutorial", isCompleted: true },
    ]);
    this.todoCounter = useState({ value: 3 });
    this.inputRef = useAutofocus("input");
  }

  addTodo(ev) {
    if (ev.keyCode === 13 && ev.target.value != "") {
      this.todos.push({
        id: this.todoCounter.value,
        description: ev.target.value,
        isCompleted: false,
      });
      this.todoCounter.value++;
      ev.target.value = "";
    }
  }

  toggleItem(id) {
    const todoTask = this.todos.find((todo) => todo.id === id);
    if (todoTask) {
      todoTask.isCompleted = !todoTask.isCompleted;
    }
  }

  deleteTodo(id) {
    const index = this.todos.findIndex((elem) => elem.id === id);
    if (index >= 0) {
      this.todos.splice(index, 1);
    }
  }
}
