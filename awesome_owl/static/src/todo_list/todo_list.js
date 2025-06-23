import { Component, onWillStart } from "@odoo/owl";
import { TodoItem } from "./todo_item";
import { useAutofocus } from "../utils";
import { TodoModel } from "./todo_model";

// Main todo list component with task management
export class TodoList extends Component {
    static template = "awesome_owl.TodoList";
    static components = { TodoItem };

    setup() {
        this.todoModel = new TodoModel();
        onWillStart(() => {
            return this.todoModel.load();
        });
        useAutofocus("input")
    }

    // Handle Enter key press in input
    handleKeypress(event) {
        if (event.key === "Enter") {
            this.addNewTask(event.target);
        }
    }

    // Add a new task from input
    createTask() {
        const inputEl = this.refs.input;
        this.addNewTask(inputEl);
        inputEl.focus();
    }

    // Helper to add a new task
    addNewTask(inputElement) {
        const taskText = inputElement.value.trim();
        if (taskText) {
            this.todoModel.createTodo(taskText);
            inputElement.value = "";
        }
    }
}
