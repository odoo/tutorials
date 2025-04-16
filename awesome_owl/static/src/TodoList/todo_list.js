import { Component, useState } from "@odoo/owl";
import { TodoItem } from "./todo_item";
import { useAutofocus } from "../utils";

export class TodoList extends Component {
  static template = "awesome_owl.todo_list";
  static components = { TodoItem };

  setup() {
    this.todos = useState([]);
    this.state = useState({ newTodo: "" });  // use object here instead of just a string
    this.inputRef = useAutofocus("inputfocus");
  }

  // Handle input change
  onInput(ev) {
    this.state.newTodo = ev.target.value;
  }

  // Add new todo when enter key is pressed
  addTodo(ev) {
    if (ev.keyCode === 13 && this.state.newTodo.trim() !== "") {
      this.todos.push({
        id: this.todos.length + 1,
        description: this.state.newTodo,
        isCompleted: false,
      });
      this.state.newTodo = "";  // Clear input field
    }
  }

  toggleTodoState(id) {
    const todo = this.todos.find(t => t.id === id);
    if (todo) {
      todo.isCompleted = !todo.isCompleted;
    }
  }

  removeTodo(todoId) {
    const index = this.todos.findIndex(task => task.id === todoId);
    if (index !== -1) {
        this.todos.splice(index, 1);
    }
  }
}
