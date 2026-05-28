import { Component, useState } from '@odoo/owl';
import { TodoItem } from '../todo_item/todo_item';
import { useAutoFocus } from '../utils';

export class TodoList extends Component {
  static template = 'awesome_owl.todo_list';
  static components = { TodoItem };

  setup() {
    this.todos = useState([]);
    this.lastId = 1;
    this.inputRef = useAutoFocus('taskInput');
  }

  addTodo(ev) {
    const value = ev.target.value.trim();
    if (value && ev.keyCode === 13) {
      this.todos.push({
        id: this.lastId++,
        description: value,
        isCompleted: false,
      });
      ev.target.value = '';
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
