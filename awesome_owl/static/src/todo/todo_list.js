/** @odoo-module **/
import { Component, useState } from "@odoo/owl";
import { TodoItem } from "./todo_item";

export class TodoList extends Component {
    static props = {};
    static template = "awesome_owl.TodoList";
    static components = { TodoItem };

    setup() {
        this.state = useState({
            todos: [
                { id: 1, description: "buy milk", isCompleted: false },
                { id: 2, description: "write report", isCompleted: true },
                { id: 3, description: "call friend", isCompleted: false },
            ]
        });
    }
}
