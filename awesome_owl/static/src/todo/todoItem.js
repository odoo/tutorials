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
        },
        toggleTodo: Function,
        removeTodo: Function,
    };

    toggleTodo(event) {
        this.props.toggleTodo(parseInt(this.props.todo.id));
    }

    removeTodo(event) {
        this.props.removeTodo(parseInt(this.props.todo.id));
    }
}
