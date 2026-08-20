import { Component, useState } from "@odoo/owl";
import { TodoItem } from "./todo_item";

export class TodoList extends Component {
  static template = "awesome_owl.todo_list";
  static components = { TodoItem };

  // { id: 2, description: "buy brocolli", isCompleted: true }
  // { id: 3, description: "buy soy milk", isCompleted: false }
  state = useState({ items: [], count: 0 });

  addTodo(ev) {
    if (ev.key === "Enter" && ev.target.value.trim() !== ""){
      this.state.items.push({ 'id': this.state.count++, 'description': ev.target.value, 'isCompleted': false });
      ev.target.value = ""
    }
  }

}
