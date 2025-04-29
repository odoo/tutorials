/** @odoo-module **/

import { Component, useState } from "@odoo/owl";

export class TodoItem extends Component {
    static template = "awesome_owl.todo_item";
    static props = {
        todo: {
            type: Object,
            shape: {
                id: Number,
                description: String,
                isCompleted: Boolean
            }
        },
        toggleState: Function,
        removeTodo: Function
    };

    onChange() {
        this.props.toggleState(this.props.todo.id);
    }

    onClick() {
        this.props.removeTodo(this.props.todo.id);
    }
}
