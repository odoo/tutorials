/** @odoo-module **/
import { Component, useState } from "@odoo/owl";
import { TodoItem } from "@awesome_owl/todo/todo_item";


export class TodoList extends Component {
  static template = "awesome_owl.TodoList";
  static components = { TodoItem };
  static props = {};

    setup() {
      this.state = useState({nextId : 0})
      this.todos = useState([]);
      this.inputRefValue = useState({ value: "" });
      this.toggleState = this.toggleState.bind(this)
      this.removeTodo = this.removeTodo.bind(this)
    }

  addTodo(ev) {
    if (ev.keyCode === 13) {
      const desc = this.inputRefValue.value.trim();
      if (!desc) return;

      this.todos.push({
        id: this.state.nextId++,
        description: desc,
        isCompleted: false,
      });

      this.inputRefValue.value = "";  
    }
  }
  toggleState(id) {
    const todo = this.todos.find((todo) => todo.id === id);
    if (todo) {
      todo.isCompleted = !todo.isCompleted;
    }
  }

  removeTodo(id) {
    const index = this.todos.findIndex((todo) => todo.id === id);
    if (index >= 0) {
      this.todos.splice(index, 1);
    }
}
}
