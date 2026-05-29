import { Component, useState } from "@odoo/owl";
import { TodoItem } from "./todo_item";

export class TodoList extends Component {
    static template = "awesome_owl.TodoList";
    static components = { TodoItem };

    setup() {
        this.todos = useState([
            { id: 3, description: "Eat", isCompleted: false },
            { id: 4, description: "Sleep", isCompleted: true },
        ]);
    }
}
