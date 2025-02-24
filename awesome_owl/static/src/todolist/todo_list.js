import { Component, useState, useRef, onMounted } from "@odoo/owl";
import { TodoItem } from "./todo_item";
import { useAutofocus } from "../utils";

export class TodoList extends Component {
  static components = { TodoItem };

  setup() {
    this.todos = useState([]);
    this.todoCounter = 1;
    // this.inputRef = useRef("taskInput");
    useAutofocus(this.inputRef);
  }

  addTodo(ev) {
    if (ev.keyCode === 13) {
      const description = ev.target.value.trim();
      if (description) {
        this.todos.push({
          id: this.todoCounter++,
          description,
          isCompleted: false,
        });
        ev.target.value = "";
      }
    }
  }

  toggleState = (todoId) => {
    const todo = this.todos.find((t) => t.id === todoId);
    if (todo) {
      todo.isCompleted = !todo.isCompleted;
    }
  };

  removeTodo = (todoId) => {
    const index = this.todos.findIndex((t) => t.id === todoId);
    if (index >= 0) {
      this.todos.splice(index, 1);
    }
  };
}

TodoList.template = "awesome_owl.todo_list";
