/** @odoo-module **/

import { Component, useState } from "@odoo/owl";

export class TodoItem extends Component {
    static template = "awesome_owl.todo_item";

    static props = {
        todoList: {
            type: Object,
            shape: {
                id: { type: Number },
                description: { type: String },
                isCompleted: { type: Boolean },
            },
            required: true,
        },
        toggleState: { type: Function, optional: true },
        removeTodo: { type: Function, optional: true },
    }


    toggleCheckbox() {
        if (this.props.toggleState) {
            this.props.toggleState(this.props.todoList.id);
        }
    }
    removeItem() {
        if (this.props.removeTodo) {
            this.props.removeTodo(this.props.todoList.id);
        }
    }
}
