import { Component, useState } from "@odoo/owl";
import { TodoItem } from "./todo_item";
import { useAutofocus } from "../utils";

export class TodoList extends Component {
    static template = "awesome_owl.TodoList";
    static components = { TodoItem };

    setup() {
        this.todos = useState([]);
        this.nextId = 1;

        // Autofocus input
        this.inputRef = useAutofocus("newTodoInput");
    }

    addTodo(ev) {
        if (ev.keyCode === 13) {
            const description = this.inputRef.el.value.trim();
            if (!description) return;

            this.todos.push({
                id: this.nextId++,
                description,
                isCompleted: false,
            });
        }
    }

    toggleTodo(todoId) {
        const todo = this.todos.find((t) => t.id === todoId);
        if (todo) {
            todo.isCompleted = !todo.isCompleted;
        }
    }

    removeTodo(todoId) {
        const index = this.todos.findIndex((t) => t.id === todoId);
        if (index >= 0) {
            this.todos.splice(index, 1);
        }
    }
}