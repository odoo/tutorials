/** @odoo-module **/

import { Component } from "@odoo/owl";

export class TodoItem extends Component {

    static template = "awesome_owl.TodoItem";

    static props = {
        todo: {
            type: Object,
            values: {
                id: Number,
                description: String,
                isCompleted: Boolean
            },
        },
        toggleState: Function,
        removeTodo: Function
    };

    onchangeCheckbox() {
        this.props.toggleState(this.props.todo.id);
    }

    onClickRemove() {
        this.props.removeTodo(this.props.todo.id);
    }
}