import { Component, useState, useRef, onMounted } from "@odoo/owl";
import { TodoItem } from "./TodoItem";

export class TodoList extends Component {
  static template = "awesome_owl.TodoList";
  static components = { TodoItem };

  setup() {
    this.todoInput = useRef("todoInput");
    console.log(this.todoInput.el)
    this.todos = useState([]);
    this.uniqueId = 1;

    onMounted(() => {
      console.log(this.todoInput.el);
      this.todoInput.el.focus();
    });
  }

  onKeyup(e) {
    const value = e.target.value.trim();

    if (!value || e.keyCode !== 13) return;

    this.todos.push({
      id: this.uniqueId++,
      description: value,
      isCompleted: false,
    });

    e.target.value = "";
  }

  toggleTodo(id) {
    const todo = this.todos.find((todo) => todo.id === id);
    console.log(todo)
    if (todo) {
      todo.isCompleted = !todo.isCompleted;
    }
  }

  removeTodo(id) {
    const index = this.todos.findIndex((todo) => todo.id === id);
    console.log(index)
    if (index >= 0) {
      this.todos.splice(index, 1);
    }
  }
}
