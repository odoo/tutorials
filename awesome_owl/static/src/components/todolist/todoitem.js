/** @odoo-module **/

import { Component } from "@odoo/owl";

export default class TodoItem extends Component {
    static template = "awesome_owl.TodoItem";
    static props = {
        todo: {
            type: Object,
            shape: {
                id: { type: Number },
                description: { type: String },
                isCompleted: { type: Boolean },
            },
        },
        toggleState:{type: Function, required: true},
        removeTodo:{type: Function, required: true}

    };
    toggleCheckbox() {
        this.props.toggleState(this.props.todo.id);
    }
    remove() {
        this.props.removeTodo(this.props.todo.id);
    }
}
