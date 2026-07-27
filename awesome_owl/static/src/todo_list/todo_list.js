import { Component, useState } from "@odoo/owl";
import { TodoItem } from "./todo_item";
import { useAutofocus } from "../utils";

export class TodoList extends Component {
    static template = "awesome_owl.TodoList";
    static components = { TodoItem };
    static props = {};

    setup() {
        this.todos = useState([]);
        this.id = 1;

        useAutofocus("input");
    }

    addTodo(event) {
        if (event.keyCode === 13) {
            const description = event.target.value.trim();
            if (description) {
                this.todos.push({
                    id: this.id++,
                    description: description,
                    isCompleted: false,
                });
                event.target.value = "";
            }
        }
    }

    toggleTodo(id) {
        const todo = this.todos.find((todo) => todo.id === id);
        if (todo) todo.isCompleted = !todo.isCompleted;
    }

    removeTodo(id) {
        const index = this.todos.findIndex((todo) => todo.id === id);
        if (index >= 0) this.todos.splice(index, 1);
    }
}
