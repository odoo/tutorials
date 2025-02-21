import { Component, useState} from "@odoo/owl";
import { TodoItem } from "./todo_item";
import { useAutofocus } from "./utils";

export class TodoList extends Component {
    static template = "awesome_owl.TodoList";
    static components = { TodoItem };

    setup() {
        this.nextId=4
        this.todos =useState( [
            { id: 1, description: "Buy milk", isCompleted: false },
            { id: 2, description: "Walk the dog", isCompleted: false },
            { id: 3, description: "Write code", isCompleted: false },
        ]);
        this.inputRef = useAutofocus(); 
    }

    addTodo(ev) {
        if (ev.keyCode === 13) {  // Check if Enter key was pressed
            const description = ev.target.value.trim(); // Get input value and remove spaces
            
            if (description) {  // Only add if input is not empty
                this.todos.push({ id: this.nextId++, description, isCompleted: false });
                ev.target.value = "";  // Clear input field
            }
        }
    }

    removeTodo(todoId) {
        const index = this.todos.findIndex((todo) => todo.id === todoId);
        if (index >= 0) {
            this.todos.splice(index, 1);
        }
    } 
}
