/** @odoo-module **/

import { Component, useState } from "@odoo/owl";

export class TodoItem extends Component {
    static template = "awesome_owl.TodoItem";
    static props = {
        id: { type: Number },
        description: { type: String },
        isCompleted: { type: Boolean },
        toggleState: { Function },
        removeTodo: { Function }
    };

    toggleState() {
        this.props.toggleState(this.props.id);
    }

    removeTodo() {
        this.props.removeTodo(this.props.id);
    }
}
