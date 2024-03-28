/** @odoo-module **/

import { Component } from "@odoo/owl";

export class TodoItem extends Component {
    static template = "awesome_owl.TodoItem";
    static props = {
        id: { type: Number },
        description: { type: String },
        isCompleted: { type: Boolean },
        onToggleCompleted: { type: Function },
        onRemove: { type: Function },
    };

    onChange() {
        this.props.onToggleCompleted(this.props.id);
    }

    onRemove() {
        this.props.onRemove(this.props.id);
    }
}
