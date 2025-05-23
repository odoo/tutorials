/** @odoo-module **/

import { Component } from "@odoo/owl";

export class TodoItem extends Component {
    static template = "awesome_owl.TodoItem";

    static props = {
        todo: {
            type: Object,
            shape: {
                id: Number,
                description: String,
                isCompleted: Boolean,
            },
        },
        onToggle: Function,
        onRemove: Function,
    };

    toggle() {
        this.props.onToggle();
    }

    onRemove() {
        this.props.onRemove();
    }
}
