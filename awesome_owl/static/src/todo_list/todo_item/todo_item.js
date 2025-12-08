/** @odoo-module **/

import { Component } from "@odoo/owl";

export class TodoItem extends Component {
    static template = "awesome_owl.todo_item";

    static props = {
        todo: {
            type: Object,
            optional: true,
        },
        toggleCallback: {
            type: Function,
            optional: true,
        },
        removeCallback: {
            type: Function,
            optional: true,
        }
    };

    toggleChange() {
        this.props.todo.isCompleted = !this.props.todo.isCompleted;
        this.props.toggleCallback?.();
    }

    removeTodo() {
        this.props.removeCallback?.(this.props.todo.id);
    }
}
