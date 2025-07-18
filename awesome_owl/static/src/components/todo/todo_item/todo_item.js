/** @odoo-module **/

import { Component } from "@odoo/owl";

export class TodoItem extends Component {
    static template = "awesome_owl.todo_item";

    static props = {
        todo: Object,
        toggleState: Function,
        removeTodo: Function,

    };
    onRemove() {
        this.props.removeTodo(this.props.todo.id);
    }
}
