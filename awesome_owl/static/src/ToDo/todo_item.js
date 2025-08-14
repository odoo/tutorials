/** @odoo-module **/

import { Component } from "@odoo/owl";

export class TodoItem extends Component {
    static props = {
        id: Number, description: String, isCompleted: Boolean, toggle: Function, removeTodo: Function
    };
    static template = "awesome_owl.todo_item";

    toggle(_) {
        this.props.toggle(this.props.id);
    }

    removeTodo(_) {
        this.props.removeTodo(this.props.id);
    }
}
