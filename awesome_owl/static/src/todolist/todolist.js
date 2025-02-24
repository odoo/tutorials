import { Component, useState } from "@odoo/owl";
import { TodoItem } from "../todoitem/todoitem";


export class TodoList extends Component {
    static template = "awesome_owl.TodoList";
    static components = {TodoItem};

    setup() {
        this.todos = useState([
            { id: 1, description: "buy milk", isCompleted: false },
            { id: 2, description: "buy wafer", isCompleted: true },
            { id: 3, description: "write tutorial", isCompleted: false },
        ]);
    }
}
