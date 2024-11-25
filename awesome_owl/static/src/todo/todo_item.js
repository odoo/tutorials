import { Component } from "@odoo/owl";

export class TodoItem extends Component {
  static template = "awesome_owl.todo_item";
  static props = {
    todo: {
      type: Object,
      shape: { id: Number, description: String, isCompleted: Boolean },
    },
    onDelete: { type: Function, optional: true },
  };

  deleteTodo() {
    this.props.onDelete(this.props.todo);
  }

  static components = { TodoItem };
}
