/** @odoo-module **/

import { Component, useState, useRef, onMounted } from "@odoo/owl";
import { TodoItem } from "./todoItem";

function useAutoFocus(refName) {
  let inputRef = useRef(refName);
  onMounted(() => {
    inputRef.el.focus();
  });
}

export class TodoList extends Component {
  static template = "awesome_owl.TodoList";
  static components = { TodoItem };

  setup() {
    this.todos = useState([]);
    this.state = useState({ text: "" });
    this.todosId = useState({ value: 1 });
    useAutoFocus("new_task_input");
  }

  _updateInputValue(event) {
    this.state.text = event.target.value;
  }

  checkPressedKey(e) {
    const value = e.target.value;
    if (value) {
      if (e.key === "Enter") {
        this.addTodo();
      }
    }
  }

  addTodo() {
    const newTodo = {
      id: this.todosId.value,
      description: this.state.text,
      isCompleted: false,
    };
    this.todos.push(newTodo);
    this.todosId.value++;
  }

  toggleCompletion(updatedTodo) {
    const index = this.todos.findIndex((t) => t.id === updatedTodo.id);
    if (index !== -1) {
      this.todos[index].isCompleted = updatedTodo.isCompleted;
    }
  }

  toggleState(id) {
    const todo = this.todos.find((t) => t.id === id);
    if (todo) {
      todo.isCompleted = !todo.isCompleted;
    }
  }

  removeTodo(id) {
    const index = this.todos.findIndex((t) => t.id === id);
    if (index !== -1) {
      this.todos.splice(index, 1);
    }
  }
}
