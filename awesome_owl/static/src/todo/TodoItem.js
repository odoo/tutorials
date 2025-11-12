/** @odoo-module **/

import { Component } from "@odoo/owl";

export class TodoItem extends Component {
    // Method to toggle completion status

    toggleTodo() {
        this.props.toggleState(this.props.todo.id);
    }

    // Method to delete the todo
    deleteTodo() {
        this.props.removeTodo(this.props.todo.id);
    }
}

// Props validation
TodoItem.props = {
    todo: {
        type: Object,
        shape: {
            id: Number,
            description: String,
            isCompleted: Boolean,
        },
    },
    toggleState: Function,  // Required for toggling completion
    removeTodo: Function,   // Required for deleting tasks
};

TodoItem.template = "todo.TodoItem";
