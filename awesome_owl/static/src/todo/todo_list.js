import { Component, useState } from "@odoo/owl";
import { TodoItem } from "./todo_item";

export class TodoList extends Component {
    static template = "awesome_owl.todo_list";
    static components = { TodoItem };

    setup() {
        this.state = useState({
            todos: [
                { id: 1, description: "Learn OWL", isCompleted: false },
                { id: 2, description: "Buy milk", isCompleted: true },
                { id: 3, description: "Write code", isCompleted: false },
            ],
        });
    }

    // Optional: Handle toggle events from TodoItem
    onTodoToggle(todo) {
        console.log(`Todo ${todo.id} toggled to ${todo.isCompleted}`);
        // The state is already updated reactively via the todo object reference
    }
    static props = {};
}
