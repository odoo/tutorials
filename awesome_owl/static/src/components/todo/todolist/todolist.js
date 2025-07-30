import { Component, useState } from "@odoo/owl"
import { TodoItem } from "../todoitem/todoitem";

export class TodoList extends Component {
    static template = "awesome_owl.todolist"
    static components = { TodoItem }
    static props = {}

    setup() {
        this.todos = useState([
            { id: 1, description: "Buy milk", isCompleted: false },
            { id: 2, description: "Walk the dog", isCompleted: true },
            { id: 3, description: "Write blog post", isCompleted: false },
            { id: 4, description: "Call mom", isCompleted: true },
            { id: 5, description: "Clean the house", isCompleted: false },
            { id: 6, description: "Pay bills", isCompleted: false },
            { id: 7, description: "Read a book", isCompleted: true },
            { id: 8, description: "Exercise", isCompleted: false }
        ]);
    }
}
