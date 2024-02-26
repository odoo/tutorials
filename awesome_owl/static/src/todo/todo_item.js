/** @odoo-module **/

import { Component, useState } from "@odoo/owl";

export class TodoItem extends Component {
    static template = "awesome_owl.todo_item";
    static props = {
        todo: {
            required: true,
            shape: {
                id: { required: true },
                description: { required: true },
                completed: { required: true },
            },
        },
    };

    setup() {
        this.state = useState({});
    }
}
