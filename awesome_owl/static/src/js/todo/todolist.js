import { Component, useState, useRef, onMounted } from "@odoo/owl";
import { TodoItems } from "./todoitems";

export class TodoList extends Component {
  static template = "awesome_owl.todolist";

  static components = { TodoItems };

  setup() {
    this.todos = useState([]);
    this.nextId = 1;
    this.myref = useRef("myInput");

    onMounted(() => {
      this.myref.el.focus();
    });
  }

  addTodo(ev) {
    if (ev.keyCode === 13) {
      const text = ev.target.value.trim();
      if (text) {
        this.todos.push({
          id: this.nextId,
          description: text,
          isComplete: false,
        });
        ev.target.value = "";
        this.nextId++;
      }
    }
  }

  toggleState(id) {
    const todo = this.todos.find((t) => t.id === id);
    if (todo) todo.isComplete = !todo.isComplete;
  }

  removeTodo(id) {
    const index = this.todos.findIndex((t) => t.id === id);
    if (index >= 0) this.todos.splice(index, 1);
  }
}
