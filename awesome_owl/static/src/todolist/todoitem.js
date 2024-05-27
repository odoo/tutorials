/** @odoo-module **/

import { Component } from "@odoo/owl";

export class TodoItem extends Component {
    static template = "awesome_owl.todoitem";
    static props = {
        todo: {
            id: { type: Number },
            description: { type: String },
            isCompleted: { type: Boolean },
        },
        removeTodo: { type: Function },
    };

    toggleState() {
        this.props.todo.isCompleted = !this.props.todo.isCompleted
    }

    removeTodo() {
        this.props.removeTodo?.(this.props.todo.id);
    }
}