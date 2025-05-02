import { Component } from "@odoo/owl";

export class TodoItem extends Component {
  static template = "awesome_owl.todoItem";
  static props = {
    todo: {
      type: Object,
      shape: {
        id: Number,
        description: String,
        isCompleted: Boolean,
      },
    },
    onToggleComplete: Function,
    onClickDelete: Function,
  };
  toggleState() {
    this.props.onToggleComplete(this.props.todo.id);
  }
  removeTask() {
    this.props.onClickDelete(this.props.todo.id);
  }
}
