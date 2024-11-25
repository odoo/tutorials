import { Component, useState, useRef } from "@odoo/owl";
import { TodoItem } from "./todo_item";
import useAutofocus from "../utils";

export class TodoList extends Component {
  static template = "awesome_owl.todo_list";
  static props = {};

  setup() {
    this.id = 1;
    this.todos = useState([]);
    this.input = useState({ value: "" });
    this.inputRef = useRef("todo_input");
    useAutofocus(this.inputRef);
  }

  addTodo(ev) {
    if (ev.keyCode === 13 && ev.target.value) {
      this.todos.push({
        id: this.id++,
        description: this.input.value,
        isCompleted: false,
      });
      this.input.value = "";
    }
  }

  removeTodo(todo) {
    const index = this.todos.findIndex((elem) => elem.id === todo.id);
    console.log(todo, index);
    if (index >= 0) {
      this.todos.splice(index, 1);
    }
  }

  static components = { TodoList, TodoItem };
}
