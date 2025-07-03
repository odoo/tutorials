/** @odoo-module **/

import { Component } from "@odoo/owl";

export class TodoItem extends Component {
    static template = "awesome_owl.TodoItem";

    static props = {
        todoTask: {
            type: Object,
            shape: {
                id: { type: Number, optional: false },
                description: { type: String, optional: false },
                isCompleted: { type: Boolean, optional: false },
            }
        },
        toggleState: { type: Function, optional: true },
        deleteTodo: { type: Function, optional: true }
    }

    onChange() {
        if (this.props.toggleState) {
            this.props.toggleState(this.props.todoTask.id)
        }
    }
    onClick() {
        if (this.props.deleteTodo) {
            this.props.deleteTodo(this.props.todoTask.id)
        }
    }
}
