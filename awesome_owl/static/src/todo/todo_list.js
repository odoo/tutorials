/** @odoo-module **/

import { Component, useState, useRef } from "@odoo/owl";
import { TodoItem } from "./todo_item";

export class TodoList extends Component {
    // Link this class to the template defined in XML
    static template = "awesome_owl.todo_list";

    // Register the TodoItem component (used inside this component)
    static components = { TodoItem };

    setup() {
        // Reactive list to hold all todo items
        // useState makes the array reactive → UI updates when this changes
        this.todos = useState([]);

        // Simple counter to assign unique IDs to new todos
        this.nextId = 1;

        // Create a reference to the input element using its t-ref name from XML
        // Will be available as this.newTodoInput.el (where el = actual DOM node)
        this.newTodoInput = useRef("newTodoInput");

        // Bind `this` to ensure the method has the correct context when triggered by DOM events
        this.addTodo = this.addTodo.bind(this);
    }

    // Event handler that triggers when a key is pressed in the input box
    addTodo(ev) {
        // Only trigger logic if the key is Enter (keyCode 13)
        if (ev.keyCode !== 13) return;

        // Get the actual DOM input element via useRef
        const input = this.newTodoInput.el;

        const description = input.value.trim();

        if (!description) return;

        // Add new todo object to the reactive state list
        // This will auto-render the new item via t-foreach
        this.todos.push({
            id: this.nextId++,        // unique ID
            description,              // task text
            isCompleted: false,       // initially not completed
        });

        // Clear the input field after adding
        input.value = "";
    }
}
