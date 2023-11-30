/** @odoo-module **/

import { Component } from "@odoo/owl";

export class Todo extends Component {
    static template = "owl_playground.todolist.todo";

    static props = {
        todo: {
            type: Object,
            shape: {
                id: Number,
                description: String,
                done: Boolean
            }
        },
        toggleState: { type: Function },
        removeTodo: { type: Function }
    }

    toggleState() {
        this.props.todo.done = !this.props.todo.done;
    }
}
