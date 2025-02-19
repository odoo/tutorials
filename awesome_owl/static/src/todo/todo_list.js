import { Component, useState } from "@odoo/owl";

import { TodoItem } from "./todo_item";

export class TodoList extends Component {
    static components = { TodoItem };
    static template = "awesome_owl.TodoList";

    setup() {
        this.todos = useState([]);
        this.nextId = 1;
    }

    addTodo(ev) {
        console.log(ev)
        if (ev.keyCode === 13) {  // Check if Enter key is pressed
            const description = ev.target.value;  // Get input value & remove spaces
            if (description) {
                this.todos.push({ id: this.nextId++, description, isCompleted: false });
                ev.target.value = "";  // Clear input field
            }
        }
    }
}
