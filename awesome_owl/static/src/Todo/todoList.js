import { Component, useState } from "@odoo/owl";
import { TodoItem } from "./todoItem";
import { useAutofocus } from "../util";

export class TodoList extends Component {
    static template = "awesome_owl.todoList";
    static components = { TodoItem };

    setup() {
        this.todos = useState([]);
        this.nextId = 1;
        useAutofocus("input");
    }

    toggleTodo(todoId) {
        const todo = this.todos.find((todo) => todo.id === todoId);
        if (todo) {
            todo.isCompleted = !todo.isCompleted;
        }
    }
    removeTodo(todoId) {
        const idx = this.todos.findIndex((todo) => todo.id === todoId);
        if (idx) {

            this.todos.splice(idx, 1)
        }
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
            id: this.nextId++,
            description,
            isCompleted: false,

        });
        ev.target.value = "";
    }
}
