/** @odoo-module **/

import { Component } from "@odoo/owl";

export class TodoItem extends Component {
    static template = "awesome_owl.TodoItem";
    static props = {
        todo: {
            type: Object,
            shape: {
                id: Number,
                description: String,
                isCompleted: Boolean
            }
        },
        onToggle: { type: Function, optional: true },
        onRemove: { type: Function, optional: true }
    };

    toggleTodo() {
        if (this.props.onToggle) {
            this.props.onToggle(this.props.todo.id);
        }
    }

    removeTodo() {
        if (this.props.onRemove) {
            this.props.onRemove(this.props.todo.id);
        }
    }
}
