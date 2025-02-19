import { Component, useState } from "@odoo/owl";

export class TodoList extends Component {
  static template = "awesome_owl.todoitem";

  static props = {
    todo: {
      type: Object,
      shape: { id: Number, description: String, isCompleted: Boolean },
    },
  };
}
