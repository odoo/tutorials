import { Component, useState } from "@odoo/owl";
import { TodoItem } from "./todo_item";

export class TodoList extends Component {
    static template = "awesome_owl.todo_list";
    static components = { TodoItem };

    setup() {
        this.todos = useState([
            { id: 1, description: "learn owl", isCompleted: true },
            { id: 2, description: "write documentation", isCompleted: false },
            { id: 3, description: "buy milk", isCompleted: false }
        ]);
    }
}
