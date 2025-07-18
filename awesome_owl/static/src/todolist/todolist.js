/** @odoo-module **/

import { Component, useState } from "@odoo/owl";
import { TodoItem } from "./todoitem";
import { useAutofocus } from "../utils/utils";

export class TodoList extends Component {
    static template = "awesome_owl.TodoList";
    static components = { TodoItem };

    setup() {
        this.state = useState({
            text: "",
            todos: [],
            nextId: 1,
        });
        this.inputRef = useAutofocus("input");
        this.toggleState = this.toggleState.bind(this);
        this.todoDelete = this.todoDelete.bind(this);
    }

    addTodo(ev) {
        if (ev.key === "Enter") {
            const description = this.state.text.trim();
            if (!description) return;

            this.state.todos.push({
                id: this.state.nextId++,
                description: description,
                isCompleted: false,
            });
            this.state.text = "";
        }
    }

    toggleState(todoId) {
        const todo = this.state.todos.find((t) => t.id === todoId);
        if (todo) {
            todo.isCompleted = !todo.isCompleted;
        }
    }
    todoDelete(todoId) {
    const index = this.state.todos.findIndex((t) => t.id === todoId);
    if (index >= 0) {
        this.state.todos.splice(index, 1);
        for (let i = index; i < this.state.todos.length; i++) {
            this.state.todos[i].id = i + 1;
        }
    }
    this.state.nextId = this.state.todos.length + 1;
    }
}
