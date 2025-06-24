/** @odoo-module **/

import { Component } from "@odoo/owl";


export class TodoItem extends Component {
    static template = "awesome_owl.todoItem";
    static props = {
        id: Number,
        description: String,
        isCompleted: Boolean,
        toggleState: Function,
        removeTodo: Function,
    };
}