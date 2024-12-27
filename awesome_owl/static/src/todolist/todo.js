import { Component } from "@odoo/owl";

export class Todo extends Component {
  static template = "awesome_owl.todo";
  static props = {
    todo: {
      description: String,
      isCompleted: Boolean,
    },
  };
}
