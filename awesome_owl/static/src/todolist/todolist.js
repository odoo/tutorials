import { Component, useState } from "@odoo/owl";
import { TodoItem } from "./todoitem";


export class TodoList extends Component {
    static template = "awesome_owl.TodoList";
    static components = { TodoItem };

    setup() {
        this.todos = useState([
            { id: 1, description: "write tutorial", isCompleted: true },
            { id: 2, description: "buy milk", isCompleted: false },
        ]);
    }
}
