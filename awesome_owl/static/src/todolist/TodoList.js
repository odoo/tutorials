import { Component, useState } from "@odoo/owl";
import { useAutofocus } from "../utils";
import { TodoItem } from "./TodoItem";

export class TodoList extends Component {
  static template = "awesome_owl.TodoList";
  static components = { TodoItem }

  setup() {
    this.id = 1
    this.todos = useState([])
    useAutofocus("input")
  }

  handleAdd(ev) {
    if (ev.keyCode !== 13 || ev.target.value === "") return

    this.todos.push({
      id: this.id++,
      description: ev.target.value,
      isCompleted: false,
    })

    ev.target.value = ""
  }

  handleToggle(todoId) {
    const todo = this.todos.find(({ id }) => id === todoId)
    if (!todo) return

    todo.isCompleted = !todo.isCompleted
  }

  handleDelete(todoId) {
    const index = this.todos.findIndex(({ id }) => id === todoId)
    if (index === -1) return

    this.todos.splice(index, 1)
  }
}
