import { Component, useState, useRef, onMounted } from "@odoo/owl";
import { Todo } from "./todo";

export class TodoList extends Component {
  static template = "awesome_owl.todolist";
  static props = {};
  static components = { Todo };

  setup() {
    this.state = useState({
      todos: [
        { id: 0, description: "buy milk", isCompleted: false },
        { id: 1, description: "drink water", isCompleted: false },
        { id: 2, description: "play soccer", isCompleted: true },
      ],
    });
    this.todoInputRef = useRef("todo_input");
    onMounted(() => {
      this.todoInputRef.el.focus();
    });
  }

  addTodo(event) {
    if (event.keyCode == 13 && event.target.value != "") {
      this.state.todos.push({
        id: this.state.todos.length,
        description: event.target.value,
        isCompleted: false,
      });
      event.target.value = "";
      console.log(this.state.todos);
    }
  }

  toggleState(id) {
    const index = this.state.todos.findIndex((todo) => todo.id == id);
    if (index != -1) {
      this.state.todos[index] = {
        ...this.state.todos[index],
        isCompleted: !this.state.todos[index].isCompleted,
      };
    }
  }
}
