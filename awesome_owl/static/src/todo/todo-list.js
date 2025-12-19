import { useState, Component } from "@odoo/owl";
import { TodoItem } from "./todo-item";

export class TodoList extends Component {
    static template = "awesome_owl.todo-list";
    static components = { TodoItem }

    setup() {
        this.state = useState([
            { id: 1, description: "buy water", isCompleted: true },
            { id: 2, description: "buy bread", isCompleted: false },
            { id: 3, description: "buy milk", isCompleted: false },
        ]);
    }
}
