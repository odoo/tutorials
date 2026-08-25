import { Component } from "@odoo/owl";

export class TodoItem extends Component {
  static template = "awesome_owl.TodoItem";
  static props = {
    todo: {
      type: Object,
      shape: {
        id: Number,
        description: String,
        isCompleted: Boolean,
      },
    },
    onToggle: Function,
    onDelete: Function,
  }

  handleToggle() {
    this.props.onToggle(this.props.todo.id)
  }

  handleDelete() {
    this.props.onDelete(this.props.todo.id)
  }
}
