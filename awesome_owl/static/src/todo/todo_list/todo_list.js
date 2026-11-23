import { Component, useState, useRef, onMounted } from "@odoo/owl";
import { TodoItem } from "../todo_item/todo_item";

export class TodoList extends Component {
  static template = "awesome_owl.todo_list";
  static components = { TodoItem };

  setup() {
    this.state = useState({
      todos: [
        { id: 1, description: "Swimming", isCompleted: false },
        { id: 2, description: "Groceries", isCompleted: true },
      ],
    });
    this.inputState = useState({ value: "" });
    this.inputRef = useRef("taskInput");
    onMounted(() => {
      this.inputRef.el?.focus();
    });
  }

  onChangeInput(event) {
    const input = event.target;
    this.inputState.value = input.value;
  }

  onKeydown(event) {
    if (event.key === "Enter") {
      this.addTodo();
    }
  }

  addTodo() {
    const description = this.inputState.value.trim();
    if (!description) return;
    const nextId =
      this.state.todos.length
        ? Math.max(...this.state.todos.map((todo) => todo.id)) + 1
        : 1;
    const newTodo = {
      id: nextId,
      description,
      isCompleted: false,
    };
    this.state.todos.push(newTodo);
    this.inputState.value = "";
  }

  toggleComplete(id) {
    const todo = this.state.todos.find((todo) => todo.id === id);
    if (todo) {
      todo.isCompleted = !todo.isCompleted;
    }
  }

  removeTodo(id) {
    this.state.todos = this.state.todos.filter((todo) => todo.id !== id);
  }
}
