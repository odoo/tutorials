import { Component, useState } from "@odoo/owl";
import { TodoItem } from "./todo_item";
import { useAutofocus } from "../utils/useAutoFocus";

export class TodoList extends Component {
  static template = "awesome_owl.TodoList";

  static components = { TodoItem };

  setup() {
    this.state = useState({
      todos: [],
      curr_id: 0,
    });

    this.inputRef = useAutofocus("input");
    this.delete_todo = this.delete_todo.bind(this);
  }

  add_todo(ev) {
    if (ev.keyCode === 13) {
      const value = ev.target.value.trim();
      if (value !== "") {
        this.state.todos.push({
          id: this.state.curr_id,
          description: value,
          isCompleted: false,
        });
      }
      ev.target.value = "";

      this.state.curr_id++;
    }
  }

  delete_todo(todo_to_remove_id) {
    const index = this.state.todos.findIndex(
      (elem) => elem.id === todo_to_remove_id
    );
    if (index >= 0) {
      this.state.todos.splice(index, 1);
    }
  }
}
