/** @odoo-module **/

import { Component } from "@odoo/owl";

export class Todo extends Component {
    static template = "owl_playground.todo";

    static props = {
        todo: {
            type: Object,
            shape: {
                id: Number,
                description: String,
                done: Boolean
            }
        }
    }
}
