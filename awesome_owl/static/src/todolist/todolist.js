import { Component, useState } from "@odoo/owl";
import { TodoItem } from "./todo_item";

export class TodoList extends Component {
    static template = "awesome_owl.TodoList";
    static components = { TodoItem };

    setup() {
        this.todos = useState([]);
    }

    addTodo(ev) {
        if (ev.keyCode === 13) {
            const description = ev.target.value.trim();

            if (!description) {
                return;
            }

            this.todos.push({
                id: this.nextId++,
                description: description,
                isCompleted: false,
            });
            
            ev.target.value = "";
        }
    }
}
