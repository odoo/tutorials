import { Component } from "@odoo/owl";

export class TodoItem extends Component {
  static template = "awesome_owl.todo_item";
  static props = {
    todo: {
      type: Object,
      shape: {
        id: { type: Number, default: 0 },
        description: { type: String },
        isCompleted: { type: Boolean },
      },
    },
    removeTodo: { type: Function, optional: true },
    toggleState: { type: Function, optional: true },
  };

  onToggle() {
    if (this.props.toggleState) {
      this.props.toggleState(this.props.todo.id);
    }
  }
  onRemoveTodo() {
    if (this.props.removeTodo) {
      this.props.removeTodo(this.props.todo.id); 
    }
  }
}
