import { Component, useState } from "@odoo/owl";
import { TodoItem } from "./todo_item";

export class TodoList extends Component {
    static template = "awesome_owl.TodoList";
    static components = { TodoItem };

    setup() {
        // Reactive state: list of todos
        this.todos = useState([
            { id: 1, description: "buy milk", isCompleted: false },
            { id: 2, description: "walk the dog", isCompleted: true },
            { id: 3, description: "read a book", isCompleted: false },
        ]);
    }
}