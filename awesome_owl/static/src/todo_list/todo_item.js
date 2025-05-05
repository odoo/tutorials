/** @odoo-module **/

import { Component, useState } from "@odoo/owl";

export class TodoItem extends Component {
    static template = "awesome_owl.todo_item";

    static props = {
        todo_list: {
            type: Object,
            shape: {
                id: { type: Number },
                description: { type: String },
                isCompleted: { type: Boolean }
            },
            required: true,
        },
        toggleState: { type: Function, optional: true }
    }

    toggleCheckbox(ev) {
        if (this.props.toggleState) {
            this.props.toggleState(this.props.todo_list.id);
        }
    }
}
