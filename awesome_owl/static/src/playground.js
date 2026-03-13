import { Component, markup, useState } from "@odoo/owl";
import { Counter } from "./components/counter/counter";
import { Card } from "./components/card/card";
import { TodoList } from "./components/todo/todoList/todoList";
import { useAutofocus } from "./js/utils";

export class Playground extends Component {
  static template = "awesome_owl.playground";
  static components = { Counter, Card, TodoList };
  static props = ["*"];

  setup() {
    this.sum = useState({ value: 2 });
    this.todos = useState([]);
    this.state = useState({ text: "", nextId: 1 });
    useAutofocus("inputTodo");
  }
  
  increaseCount() {
    this.sumvalue++;
  }

  addTodo(ev) {
    if (ev.key === "Enter") {
      if (this.state.text === "") return;
      this.todos.push({
        id: this.state.nextId++,
        description: this.state.text,
        isCompleted: false,
      });
      this.state.text = "";
    }
  }
  deleteTodo(id) {
    const index = this.todos.findIndex((todo) => todo.id === id);
    if (index !== -1) {
      this.todos.splice(index, 1);
    }
  }
  markAsCompleted(todo) {
    todo.isCompleted = true;
  }

  html = markup("<h4>Improve Your Self</h4>");
}
