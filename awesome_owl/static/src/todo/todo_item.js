/** @odoo-module **/

import { Component } from "@odoo/owl";

export class TodoItem extends Component {
    static props = {
        todo: {
            id: Number,
            description: String,
            isCompleted: Boolean,
        },
        toggleState: {
            type: Function,
            optional: true
        },
        removeTodo: {
            type: Function,
            optional: true
        }
    };
    static template = "awesome_owl.todo_item";
}
