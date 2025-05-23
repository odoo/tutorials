/** @odoo-module **/

import { Component, useState } from "@odoo/owl";
import { TodoItem } from "./todo_item.js";

export class TodoList extends Component {
    static template = "awesome_owl.todo_list";
    static components = { TodoItem };

    setup() {
        this.todos = useState([
            { id: 1, description: "Hello world", isCompleted: true },
            { id: 2, description: "Find out", isCompleted: false }
        ]);
    }
}
