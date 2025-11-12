/** @odoo-module **/

import { Component } from "@odoo/owl";

export class TodoItem extends Component {
    static template = "awesome_owl.todo_item";
    static props = {
        todo: {
            type: Object,
            shape: {
                id: Number,
                description: String,
                isCompleted: Boolean,
            },
            optional: false,
        },
        markCompleted: Function,
        deleteTodo: Function,
    };

    toggleState() {
        this.props.markCompleted(this.props.todo.id)
    }

    deleteTodo() {
        this.props.deleteTodo(this.props.todo.id);
    }
}
