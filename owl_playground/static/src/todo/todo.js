/** @odoo-module **/

import { Component } from "@odoo/owl";

export class Todo extends Component {}

Todo.template = "owl_playground.todo";
Todo.props = {
    id: { type: Number },
    description: { type: String },
    done: { type: Boolean },
};