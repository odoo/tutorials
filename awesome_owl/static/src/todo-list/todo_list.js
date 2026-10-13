import { Component, useState } from "@odoo/owl";
import { TodoItem } from "./todo_item";

export class TodoList extends Component {
    static template = "awesome_owl.todolist";
    static components = { TodoItem };

    setup() {
        this.todos = useState([
            {
                id: 1,
                description: "This is my first todo",
                isCompleted: true
            },
            {
                id: 2,
                description: "This is my second todo",
                isCompleted: false
            },
        ]);
    }
}
