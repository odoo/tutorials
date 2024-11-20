/** @odoo-module **/

import { Component } from "@odoo/owl";

export class TodoItem extends Component {
    static props = {
        id: { type: Number },
        description: { type: String },
        isCompleted: { type: Boolean },
        toggleState: { type: Function },
        remove: { type: Function }
    };

    static template = "awesome_owl.todo_item";
}
