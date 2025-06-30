/** @odoo-module **/

// Import Component base class from Owl
import { Component } from "@odoo/owl";

// Define the TodoItem component
export class TodoItem extends Component {
  // Link this component to its XML template
  static template = "awesome_owl.todo_item";

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
  };
}
