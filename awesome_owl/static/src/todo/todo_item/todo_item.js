/** @odoo-module **/

import { Component, useState } from "@odoo/owl";

export class TodoItem extends Component {
    static template = "awesome_owl.todo_item";

    static props = {
        todo: {type: { id: Number, description: String, isCompleted: Boolean }},
        toggleState: Function,
        removeTodo: Function,
    }
}
