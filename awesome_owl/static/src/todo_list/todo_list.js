import { Component, useState} from "@odoo/owl";
import { TodoItem } from "./todo_item"; // Import TodoItem
import { useAutofocus } from "../utils";

export class TodoList extends Component {
    static template = "awesome_owl.TodoList";
    static components = { TodoItem }; // Register TodoItem component

    setup() {
        // Initialize the list of todos with some hardcoded data
        this.todos = useState([]);
        this.idCounter = useState({count : 1});
        const inputRef = useAutofocus("input");
    }
    addTodo(ev) {
        // Check if the 'Enter' key was pressed (keyCode 13)
        if (ev.key === "Enter") {
            const description = this.inputRef.el.value.trim(); // Get input value
            // Don't add if the input is empty
            if (!description) return;
            // Add a new todo with a unique id
            this.todos.push({
                id: this.idCounter.count++, // Increment the id for uniqueness
                description: description,
                isCompleted: false,
            });
            // Clear the input field
            this.inputRef.el.value = "";
        }
    }
}
