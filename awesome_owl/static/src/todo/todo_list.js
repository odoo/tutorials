import { Component, useState, useRef, onMounted } from "@odoo/owl";
import { useAutofocus } from "../util";
import { TodoItem } from "./todo_item";

export class TodoList extends Component {
  static template = "awesome_owl.todolist";

  setup() {
    this.todos = useState([]);
    useAutofocus("task_input");
  }

  addTodo(ev) {
    if (ev.keyCode == 13 && ev.target.value != "") {
      this.todos.push({
        id: this.todos.length + 1,
        description: ev.target.value.toString(),
        isCompleted: false,
      });
      ev.target.value = "";
    }
  }
  
  removeTodo(id) {  
    this.todos.splice(0,this.todos.length,...this.todos.filter((todo) => todo.id !== id))
  }

  toggleState(id) {
    this.todos.splice(0,this.todos.length,...this.todos.map((todo) =>
      id === todo.id ? { ...todo, isCompleted: !todo.isCompleted } : todo
    ))
  }

  static components = { TodoItem };
}
