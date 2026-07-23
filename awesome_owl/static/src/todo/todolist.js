import { Component, useState } from "@odoo/owl";
import { TodoItem } from "./todoitem";

export class TodoList extends Component {
    static template = "awesome_owl.todolist";
    static components = { TodoItem };

    setup() {
        // this.todos = useState([
        //     { id: 3, description: "buy milk", isCompleted: false },
        //     { id: 4, description: "FIX MACHINE PLX", isCompleted: false },
        //     { id: 5, description: "WAKE UP", isCompleted: true },
        // ]);
        this.todos = useState([]);
    }

    addTodo(event) {
        // console.warn("addTodo");
        // console.log(event);
        if (event.keyCode === 13) {
            let description = event.target.value;
            if (description.length == 0) {
                return;
            }
            let next_id = 1 + Math.max(...this.todos.map(item => item.id), 0);
            this.todos.push({ id: next_id, description: description, isCompleted: false });
            // Reset input
            event.target.value = '';
        }
    }
}