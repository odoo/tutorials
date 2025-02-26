import { Component, useState } from "@odoo/owl";
import { TodoItem } from "./todo_item";

export class TodoList extends Component {
    static template = "awesome_owl.todo_list";
    static components = { TodoItem };

    setup() {
        this.state = useState({
            todos: [], // Start with an empty array instead of hardcoded values
            newTask: "", // Reactive state for the input
        });
        this.nextId = 1; // Counter for unique IDs
    }

    // Optional: Handle toggle events from TodoItem
    onTodoToggle(todo) {
        console.log(`Todo ${todo.id} toggled to ${todo.isCompleted}`);
    }
    static props = {};

    addTodo(ev) {
        if (ev.keyCode == 13) { // Check if Enter was pressed
            const description = this.state.newTask.trim(); // Trim whitespace
            if (description) { // Only proceed if input is non-empty
                this.state.todos.push({
                    id: this.nextId++, // Assign and increment the ID
                    description: description,
                    isCompleted: false,
                });
                this.state.newTask = ""; // Clear the input
            }
        }
    }
}
