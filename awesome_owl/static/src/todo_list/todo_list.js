import { Component, useState } from "@odoo/owl";
import { TodoItem } from "./todo_item";
export class TodoList extends Component {
  static template = "awesome_owl.TodoList";

  static components = { TodoItem };

  setup() {
    this.state = useState({
      todos: [],
      curr_id: 0,
    });
  }

  add_todo(ev) {
    if (ev.keyCode === 13) {
      var value = ev.target.value.trim();
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
}
