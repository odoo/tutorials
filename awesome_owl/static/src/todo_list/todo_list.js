import {Component, useState} from "@odoo/owl";
import {TodoItem} from "./todo_item";

export class TodoList extends Component {
    static template = "awesome_owl.todo_list";
    static components = {TodoItem};

    setup() {
        this.todos = useState([
            {id: 1, description: "abcd", isCompleted: true},
            {id: 2, description: "abcd", isCompleted: false},
        ]);

    }

    addTodo(ev) {
        if (ev.key !== "Enter") {
            return;
        }

        const description = ev.target.value.trim();

        if (!description) {
            return;
        }

        this.todos.push({
            id: Math.max(0, ...this.todos.map(todo => todo.id)) + 1,
            description: description,
            isCompleted: false,
        });

        ev.target.value = "";
    }
}
