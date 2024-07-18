/** @odoo-module **/

import { Component } from "@odoo/owl";

export class TodoItem extends Component {
    static template = "awesome_owl.TodoItem";

    toggleTodo() {
        this.props.toggle(this.props.todo)
    }
    removeTodo() {
        this.props.remove(this.props.todo)
    }
}
