import { Component, useState } from "@odoo/owl";
import { TodoItem } from "./todo_item";

export class TodoList extends Component {
    static template = "awesome_owl.TodoList"
    static components = { TodoItem }
    id = 1;

    setup () {
        this.todos = useState([]);
    }

    addTask(event) {
        const { target: { value }, keyCode } = event;
        if (keyCode != 13 || !value.trim()) return;
        this.todos.push({
            id: this.id++,
            description: value,
            isCompleted: false,
        });
        event.target.value = '';
    }
}
