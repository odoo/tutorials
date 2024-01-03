/** @odoo-module **/

import { Component, useState } from "@odoo/owl";
import { TodoItem } from "../todo_item/todo_item";

export class TodoList extends Component {
    static template = "awesome_owl.todo_list";
    static components = { TodoItem };

    setup() {
        this.todos = useState([
            { id: 1, description: "buy milk", isCompleted: false },
            { id: 2, description: "send email", isCompleted: false },
            { id: 3, description: "buy more stuff", isCompleted: false },
            { id: 4, description: "casino", isCompleted: false }
        ]);
    }
}