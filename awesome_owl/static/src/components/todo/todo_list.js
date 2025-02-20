import { Component, useState, useRef } from "@odoo/owl";
import { TodoItem } from "./todo_item";
import { useAutofocus } from "../../utils";

export class TodoList extends Component {
  static template = "awesome_owl.todo_list";
  static components = { TodoItem };
  static props = {};

  setup() {
    this.todos = useState([]);
    this.todoCounterId = 0;

    this.inputRef = useRef("inputRef");

    useAutofocus(this.inputRef);
  }

  addTodo(event) {
    if (event.keyCode == 13) {
      const newTask = event.target.value.trim();

      if (newTask) {
        this.todos.push({
          id: this.todoCounterId,
          description: newTask,
          isCompleted: false,
        });
        this.todoCounterId++;
        event.target.value = "";
      }
    }
    this.todos.push();
  }

  removeTodo = (removeTodoId) => {
    const index = this.todos.findIndex((todo) => todo.id === removeTodoId);
    if (index !== -1) {
      this.todos.splice(index, 1);
    }
  };

  toggleTodoState(todoId) {
    const todo = this.todos.find((t) => t.id === todoId);
    if (todo) {
      todo.isCompleted = !todo.isCompleted;
    }
  }
}
