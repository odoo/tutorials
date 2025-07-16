/** @odoo-module **/

import { Component, xml } from "@odoo/owl";

export class TodoItem extends Component {
    static template = xml/* xml */`
        <div>
            <t t-esc="props.todo.id"/> .
            <t t-esc="props.todo.description" />
        </div>
    `;

    static props = {
        todo: {
            type: Object,
            shape: {
                id: Number,
                description: String,
                isCompleted: Boolean,
            },
            optional: false,
        },
    };
}