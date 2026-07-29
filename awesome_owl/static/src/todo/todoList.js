import { Component, useState } from "@odoo/owl"
import { TodoItem } from "./todoItem";

export class TodoList extends Component {
    static template = 'awesome_owl.todoList';

    setup() {
        this.todos = useState([
            { id: 2, description: "wash the dishes", isCompleted: true },
            { id: 3, description: "buy milk", isCompleted: false },
        ]);
    }

    static components = { TodoItem };
}
