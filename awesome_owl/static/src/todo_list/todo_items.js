/** @odoo-module **/

import { Component } from "@odoo/owl";

export class TodoItem extends Component {
    static template = "awesome_owl.todo_item";
    static props = {
        todo: {
            type: Object,
            shape: {
                id: { type: Number, optional: false },
                description: { type: String, optional: false },
                isCompleted: { type: Boolean, optional: false },
            },
            optional: false,
        },
        toggleState: { type: Function, optional: false },
        removeTodo: { type: Function, optional: false }, // New callback prop for deletion
    };

    toggleState() {
        // Call the parent's toggleState function with the todo id
        this.props.toggleState(this.props.todo.id);
    }

    removeTodo() {
        // Call the parent's removeTodo function with the todo id
        this.props.removeTodo(this.props.todo.id);
    }
}
