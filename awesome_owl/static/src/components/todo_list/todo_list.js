import { Component, useState, onMounted, useRef } from "@odoo/owl";
import { TodoItem } from "./todo_item/todo_item";

export class TodoList extends Component {
  static template = "awesome_owl.todolist";
  static components = { TodoItem };

  setup() {
    this.todos = useState([
      { id: 1, description: "buy milk", isCompleted: true },
      { id: 2, description: "buy Cake", isCompleted: false },
      { id: 3, description: "buy Wood", isCompleted: false },
    ]);

    this.inputRef = useRef("add_todo_input");
    onMounted(() => {
      this.inputRef.el && this.inputRef.el.focus();
    });

    this.toggleTodoState = this.toggleTodoState.bind(this);
    this.removeTodo = this.removeTodo.bind(this);
  }

  checkKey(event) {
    // event.keyCode is deprecated
    if (event.key === "Enter") {
      this.insertTodo(event.target.value);
      event.target.value = "";
    }
  }

  insertTodo(todoMsg) {
    if (todoMsg.length !== 0) {
      let newTodo = {
        id: this.todos.at(-1).id + 1,
        description: todoMsg,
        isCompleted: false,
      };

      this.todos.push(newTodo);
    }
  }

  toggleTodoState(id) {
    const todo = this.todos.find((todo) => todo.id === id);
    if (todo) {
      todo.isCompleted = !todo.isCompleted;
    }
  }

  removeTodo(id) {
    const index = this.todos.findIndex((todo) => todo.id === id);
    this.todos.splice(index, 1);
  }
}
