/** @odoo-module **/

import { Component } from "@odoo/owl";
import { TodoItem } from "./todo_item";

export class TodoList extends Component {
    static template = "awesome_owl.todo_list";
    static components = { TodoItem };

    todos = [
        {
            id: 1,
            description: "Write tutorial",
            completed: true,
        },
        {
            id: 2,
            description: "Buy milk",
            completed: false,
        }
    ];
}
