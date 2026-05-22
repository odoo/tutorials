import { Component, useState, xml } from "@odoo/owl";
import { TodoItem } from "./TodoItem";
import { useAutofocus } from "./utils";

export class TodoList extends Component {
  static template = xml`<div>
	<h1>TodoList</h1>
    <input placeholder="Add a todo" t-ref="inputRef" t-on-keyup="_addTodo"/>
    <ul t-foreach="state.todos" t-as="todo" t-key="todo.id" >
      <TodoItem todo="todo" toggle.bind="_toggle" delete.bind="_delete"/>
    </ul>
</div>`;
  static components = { TodoItem };

  setup() {
    this.state = useState({
      todos: [],
    });
    useAutofocus("inputRef");
  }

  _addTodo(event) {
    if (event.key === "Enter" && event.target.value) {
      this.state.todos.push({
        id: this.state.todos.length + 1,
        description: event.target.value,
        isCompleted: false,
      });
      event.target.value = "";
    }
  }

  _toggle(id, isCompleted) {
    const todoIndex = this.state.todos.findIndex((todo) => todo.id === id);

    if (todoIndex == -1) {
      throw new Error("Cannot find the todo");
    }

    this.state.todos[todoIndex] = {
      ...this.state.todos[todoIndex],
      isCompleted,
    };
  }

  _delete(id) {
    const todoIndex = this.state.todos.findIndex((todo) => todo.id === id);

    if (todoIndex == -1) {
      throw new Error("Cannot find the todo");
    }

    this.state.todos.splice(todoIndex, 1);
  }
}
