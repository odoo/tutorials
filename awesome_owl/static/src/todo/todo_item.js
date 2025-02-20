import { Component } from "@odoo/owl";

export class TodoItem extends Component {
  static template = "awesome_owl.todoitem";

  static props = {
    todo: {
      type: Object,
      shape: { id: Number, description: String, isCompleted: Boolean },
    },
    toggleState: Function,
    removeTodo: Function
  };
}
