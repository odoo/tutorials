/** @odoo-module **/

import { Component, useState } from "@odoo/owl";

export class TodoItem extends Component {
    static template = "awesome_owl.todoitem";
    static props = {
        todo: {
            type: Object, shape: {
                id: Number,
                description: String,
                isCompleted: Boolean,
            }},
        removeTodo: {
            type: Function,
        },
    };

    remove() {
        this.props.removeTodo(this.props.todo.id); 
    }
}
