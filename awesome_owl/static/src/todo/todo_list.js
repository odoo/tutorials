import { Component, useState } from "@odoo/owl";
import { TodoItem } from "./todo_item";
import { useAutoFocus } from "../utils"

export class TodoList extends Component {
  static template = "awesome_owl.todo_list";
  static components = { TodoItem };


  setup() {
    this.state = useState({ items: [], count: 0 });
    useAutoFocus("todo-input");
    this.toggleItemState = this.toggleItemState.bind(this);
  }

  addTodo(ev) {
    if (ev.key === "Enter" && ev.target.value.trim() !== ""){
      this.state.items.push({ 'id': this.state.count++, 'description': ev.target.value, 'isCompleted': false });
      ev.target.value = "";
    }
  }

  toggleItemState(id) {
    const item = this.state.items.find(item => item.id == id);
    item['isCompleted'] = !item['isCompleted'];
  }


}
