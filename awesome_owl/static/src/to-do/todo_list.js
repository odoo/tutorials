/** @odoo-module **/

import { Component, useState } from "@odoo/owl";
import { TodoItem } from "./todo_item";

export class TodoList extends Component {
    static template = "awesome_owl.TodoList";
    static Component = { TodoItem };

    setup() {
        this.todo = useState ([
            {id: 2, description: "write tutorial", isComplete: true},
            {id: 3, description: "buy milk", isComplete: false}
        ]);
    }
}