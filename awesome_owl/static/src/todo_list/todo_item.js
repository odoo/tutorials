/** @odoo-module **/

import {Component} from "@odoo/owl";

export class TodoItem extends Component {
    static template = "awesome_owl.TodoItem";
    static props = {
        todo: {
            type: Object,
            shape: {
                id: Number,
                description: String,
                isCompleted: Boolean,
            }
        },
        toggleState: Function,
    };

    onChange() {
        // Call the function passed as prop
        this.props.toggleState(this.props.todo.id);
    }

}