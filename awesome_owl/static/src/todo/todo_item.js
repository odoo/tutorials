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
                isCompleted: Boolean
            }
        },
        removeFromList: Function
    };

    toggleState() {
        this.props.todo.isCompleted = !this.props.todo.isCompleted;
    }

    removeTodo() {
        let todoId = this.props.todo.id;
        this.props.removeFromList(todoId);
    }
}
