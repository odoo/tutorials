import { Component, useState } from "@odoo/owl";
import { TodoItem } from "./todo_item";
import { useAutoFocus } from "../utils";

export class TodoList extends Component {
  static template = "awesome_owl.TodoList";
  static components = { TodoItem };

  setup() {
    this.nextId = 1;
    this.todos = useState([]);
    useAutoFocus("input");
  }

  addTodo(e) {
    if (e.keyCode === 13 && e.target.value !== "") {
      this.todos.push({
        id: this.nextId++,
        description: e.target.value,
        isCompleted: false,
      });
      e.target.value = "";
    }
  }

  toggleTodo(todoId) {
    const todo = this.todos.find((todo) => todo.id === todoId);
    if (todo) {
      todo.isCompleted = !todo.isCompleted;
    }
  }

  removeTodo(todoId){
    const todoIndex = this.todos.findIndex((todo)=> todo.id === todoId);
    if(todoIndex >=0 ){
        this.todos.splice(todoIndex,1)
    }
  }
}
