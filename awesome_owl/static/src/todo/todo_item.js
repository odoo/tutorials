/** @odoo-module **/

import { Component, useState } from "@odoo/owl";

export class TodoItem extends Component {
    static template = "awesome_owl.todo_item";
    static proprs = {
        todo: {
            type: Object,
            shape: {
                id: Number,
                description: String,
                isCompleted: Boolean,
            },
        },
        toggleState: {
            type: Function,
            optional: true
        },
        onRemove: {
            type: Function,
            optional: true
        }
    }

    onChange() {
        if (this.props.toggleState) {
            this.props.toggleState(this.props.todo.id)
        }
    }

    removeTodo() {
        if (this.props.onRemove) {
            this.props.onRemove(this.props.todo.id)
        }
    }
}
