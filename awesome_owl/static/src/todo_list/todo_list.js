import { Component, useState } from "@odoo/owl";
import { TodoItem } from "./todo_item"; // Import TodoItem
import { useAutofocus } from "../utils";

export class TodoList extends Component {
    static template = "awesome_owl.TodoList";
    static components = { TodoItem }; // Register TodoItem component

    setup() {
        // Initialize the list of todos with some hardcoded data
        this.todos = useState([]);
        this.idCounter = useState({ count: 1 });
        useAutofocus("input");
    }

    addTodo(ev) {
        if (ev.key === "Enter") {
            const description = ev.target.value.trim(); // Get input value
            if (!description) return;
            this.todos.push({
                id: this.idCounter.count++, // Increment the id for uniqueness
                description: description,
                isCompleted: false,
            });
            ev.target.value = "";
        }
    }

    toggleTodoState = (todoId) => {
        const todo = this.todos.find((t) => t.id === todoId);
        if (todo) {
            todo.isCompleted = !todo.isCompleted;  // Toggle the isCompleted state
        }
    }

    removeTodo = (todoId) => {
        const index = this.todos.findIndex((todo) => todo.id === todoId);
        if (index >= 0) {
            this.todos.splice(index, 1); // Remove from array
        }
    }
}
