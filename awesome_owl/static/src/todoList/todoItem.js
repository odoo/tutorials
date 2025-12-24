import { Component } from "@odoo/owl";
export class TodoItem extends Component {
  static template = "awesome_owl.TodoItem";
  static props = {
    todo: {
      type: Object,
      shape: {
        id: { type: Number },
        description: { type: String },
        isCompleted: { type: Boolean },
      },
    },
    toggleState: { type: Function },
    removeTodo: { type: Function },
  };

  onChange() {
    if (this.props.toggleState) {
      this.props.toggleState(this.props.todo.id);
    }
  }

  onremoveTodo() {
    if (this.props.removeTodo) {
      this.props.removeTodo(this.props.todo.id);
    }
  }
}
