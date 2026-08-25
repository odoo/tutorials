import { Component, useState } from "@odoo/owl";

import { TodoItem } from "./todo_item";

export class TodoList extends Component {
    static template = "awesome_owl.todo_list";
    static components = { TodoItem };

    setup() {
        this.todos = useState([]);
    }

    addTodo(event) {
        if (event.keyCode === 13) {
            const lastElement = this.todos.slice(-1)?.[0]
            const lastId = lastElement?.id ?? 0
            this.todos.push({ id: lastId + 1, description: event.target.value, isCompleted: false });
            event.target.value = ""
        }
    }
}
