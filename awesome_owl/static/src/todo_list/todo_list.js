import { Component, useState } from "@odoo/owl";
import { TodoItem } from "@awesome_owl/todo_list/todo_item";
import { useAutofocus } from "@awesome_owl/utils";

export class TodoList extends Component {
  static template = "awesome_owl.todolist";
  static components = { TodoItem };

  setup() {
    this.state = useState({
      newTaskDescription: "",
      todos: [],
      nextId: 1,
    });
    this.toggleTodo = this.toggleTodo.bind(this);
    useAutofocus("input");
    this.removeTodo = this.removeTodo.bind(this);
  }

  addTodo(ev) {
    if (ev.keyCode === 13 && this.state.newTaskDescription.trim() !== "") {
      this.state.todos.push({
        id: this.state.nextId,
        description: this.state.newTaskDescription.trim(),
        isCompleted: false,
      });
      this.state.newTaskDescription = "";
      this.state.nextId += 1;
    }
  }

  toggleTodo(id) {
    const todo = this.state.todos.find((t) => t.id === id);
    if (todo) {
      todo.isCompleted = !todo.isCompleted;
    }
  }
  removeTodo(id) {
    const index = this.state.todos.findIndex((t) => t.id === id);
    if (index >= 0) {
      this.state.todos.splice(index, 1);
    }
  }
}
