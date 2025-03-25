import { Component, useState } from "@odoo/owl";
import { TodoItem } from "./todo_item";


export class TodoList extends Component {
    static template = "awesome_owl.TodoList";
    static components = { TodoItem };
    static props = {};

    setup() {
        this.todos = useState([
            { id: 1, description: "buy milk", isCompleted: false },
            { id: 2, description: "finish Odoo project", isCompleted: true },
            { id: 3, description: "call plumber", isCompleted: false },
        ]);
    }
}
