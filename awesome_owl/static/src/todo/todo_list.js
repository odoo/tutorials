import { Component, useState } from "@odoo/owl";
import { TodoItem } from "./todo_item";

export class TodoList extends Component {
  static template = "awesome_owl.todo_list";
  static components = { TodoItem };

  state = useState({ items: [{ id: 2, description: "buy brocolli", isCompleted: true }, { id: 3, description: "buy milk", isCompleted: false }] });

}
