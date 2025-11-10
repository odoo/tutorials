import { Component } from "@odoo/owl";

export class TodoItem extends Component {
  static template = "awesome_owl.TodoItem";
  static props = {
    todos: {
      type: Object,
      shape: {
        id: Number,
        description: String,
        isCompleted: Boolean,
      },
    },
  };
}
