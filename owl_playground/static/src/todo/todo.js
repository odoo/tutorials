/** @odoo-module **/

import { Component, useState } from "@odoo/owl";

export class Todo extends Component {
    onClick() {
        this.props.toggleState(this.props.id);
    }
    static template = "owl_playground.todo";
    static props = {
        id: {type: Number},
        description: {type: String},
        done: Boolean,
        toggleState: { type: Function },
    }
}
