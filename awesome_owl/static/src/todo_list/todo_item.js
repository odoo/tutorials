/** @odoo-module **/

import { Component } from "@odoo/owl";
import { Todo } from "./todo";

export class TodoItem extends Component {
    static template = "awesome_owl.todoitem";
    static props = {
        todo: { type: Todo },
        remove: { type: Function, optional: true }
    };

    onClick() {
        if (this.props.remove) {
            this.props.remove(this.props.todo.id)
        }
    }
}
