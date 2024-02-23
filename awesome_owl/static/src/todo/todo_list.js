/** @odoo-module **/
import { Component, useState, onMounted, useRef } from "@odoo/owl";
import { TodoItem } from "./todo_item";

export class TodoList extends Component {
  static template = "awesome_owl.todo_list";
  static components = { TodoItem };

  setup() {
    this.todos = useState([]);
    this.todoId = 0;
    this.todoInputRef = useRef("ref_todo_input");
    onMounted(() => {
      this.todoInputRef.el.focus();
    });
  }

  addTodo(ev) {
    if (ev.keyCode === 13 && ev.target.value.trim() !== "") {
      this.todos.push({
        id: this.todoId,
        description: ev.target.value,
        isCompleted: false,
      });
      ev.target.value = "";
      this.todoId++;
    }
  }

  toggleState(id) {
    const todo = this.todos[id];
    todo.isCompleted = !todo.isCompleted;
  }
}
