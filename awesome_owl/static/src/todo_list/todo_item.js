/** @odoo-module */

import { Component } from "@odoo/owl";

export class TodoItem extends Component {
    static template = "awesome_owl.TodoItem";
    static props = {
        todo: {
            type: Object,
            shape: { id: Number, description: String, isCompleted: Boolean }
        },
        toggleStatus: {
            type: Function
        },
        removeTask: {
            type: Function
        }
    };

    onChange() {
        this.props.toggleStatus(this.props.todo.id);
    }

    removeTask() {
        this.props.removeTask(this.props.todo.id);
    }
}
