import { Component } from "@odoo/owl";

export class TodoItem extends Component {
  static template = "awesome_owl.TodoItem";

  setup() {
    this.toggleState = this.toggleState.bind(this);
  }

  static props = {
    todo: {
      type: Object,
      shape: { id: Number, description: String, isCompleted: Boolean },
    },
    remove_fct: { type: Function },
  };

  toggleState() {
    this.props.todo.isCompleted = !this.props.todo.isCompleted;
  }
}
