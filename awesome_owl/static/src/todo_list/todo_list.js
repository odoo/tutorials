import { Component, useState } from "@odoo/owl";
import { TodoItem } from "./todo_item";
import { useAutofocus } from "../utils";

export class TodoList extends Component {
    static template = "awesome_owl.TodoList";
    static components = { TodoItem };

    setup() {
        this.nextId = 0;
        this.state = useState({
            todos: [],
        });
        useAutofocus("input");
    }

    addTodo(ev) {
        if (ev.keyCode === 13 && ev.target.value != "") {
            this.state.todos.push({
                id: this.nextId++,
                description: ev.target.value,
                isCompleted: false,
            });
            ev.target.value = "";
        }
    }
}
