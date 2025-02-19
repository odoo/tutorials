import { Component, useState } from "@odoo/owl"
import { TodoItem } from "./todo_item";

export class TodoList extends Component {
    static template = "awesome_owl.todo_list";
    static components = { TodoItem };

    setup() {
        this.todos = useState([
            { id: 1, description: " Buy milk", isCompleted: false },
            { id: 2, description: " Walk the dog", isCompleted: true },
            { id: 3, description: " Finish Odoo project", isCompleted: false },
        ]);
    }
}
