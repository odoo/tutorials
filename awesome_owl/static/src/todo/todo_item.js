/** @odoo-module **/

import { Component } from "@odoo/owl";

export class TodoItem extends Component {
    static template = "awesome_owl.todo_item";
    static props = {
        item: { type: Object, shape: { id: Number, description: String, isCompleted: Boolean } },
        onDelete: { type: Function, optional: true },
    };

    toggleCompleted() {
        this.props.item.isCompleted = !this.props.item.isCompleted;
    }

    onDelete() {
        this.props.onDelete?.(this.props.item.id);
    }
}
