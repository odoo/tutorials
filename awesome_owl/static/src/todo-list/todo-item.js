/** @odoo-module **/

import { Component, useState } from "@odoo/owl";

export class TodoItem extends Component {
    static template = "awesome_owl.TodoItem";
    static props = {
        todo: {
            type: Object,
            shape: { id: Number, description: String, isCompleted: Boolean }
        },
        toggleState: Function,
        removeTodo: Function
    };

    _onChange() {
        this.props.toggleState(this.props.todo.id);
    }

    _onClick() {
        this.props.removeTodo(this.props.todo.id);
    }

}
