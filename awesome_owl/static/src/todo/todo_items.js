/** @odoo-module **/

import { Component } from "@odoo/owl";

export class TodoItems extends Component {
    static template = "awesome_owl.todo_items"
    static props = {
        todo_lists: { type: Array, element: { type: Object, shape: { id: Number, description: String, isCompleted: Boolean } } },
        delete_task: { type: Function },
        toggle_task: { type: Function },
    }
}
