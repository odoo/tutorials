/** @odoo-module **/

// Import Component base class from Owl
import { Component } from "@odoo/owl";

// Define the TodoItem component
export class TodoItem extends Component {
  // Link this component to its XML template
  static template = "awesome_owl.todo_item";

  onToggle() {
    // Call parent callback with this todo's id
    this.props.toggleState(this.props.todo.id);
  }

  // Trigger parent remove callback
  onRemove() {
    if (this.props.removeTodo) {
      this.props.removeTodo(this.props.todo.id);
    }
  }

  // Declare expected props and validate their structure
  static props = {
    todo: {
      type: Object,                 // Expect an object
      shape: {
        id: Number,                 // Must have a numeric 'id'
        description: String,        // Must have a string 'description'
        isCompleted: Boolean,       // Must have a boolean 'isCompleted'
      },
      optional: false,              // This prop is required; component won't work without it
    },
    toggleState: { type: Function, optional: false },
    removeTodo: { type: Function, optional: false },
  };
}
