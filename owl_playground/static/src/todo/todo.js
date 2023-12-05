/** @odoo-module */

import { Component } from "@odoo/owl";

export class Todo extends Component {
    static template = "owl_playground.Todo";
    static props = {
        id: Number,
        description: String,
        done: Boolean,
        toggleState: Function,
    };

    toggleClick(ev) {
        this.props.toggleState(this.props.id);
    }
}
