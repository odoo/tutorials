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
    onToggle: {
      type: Function,
      optional: true,
    },
    onDelete: {
      type: Function,
      optional: true,
    },
  };
}
