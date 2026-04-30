import { Component, useState } from "@odoo/owl";
import { TodoItem } from "../todo_item/todo_item";
import { useAutofocus } from "../utils";

export class TodoList extends Component {
    static template = "awesome_owl.TodoList";
    static components = { TodoItem };
    static props = {};

    setup() {
        this.todos = useState([]);
        this.nextId = 0;
        this.inputRef = useAutofocus("todoInput");
    }

    toggleTodo(todoId) {
        const todo = this.todos.find((t) => t.id === todoId);
        if (todo) {
            todo.isCompleted = !todo.isCompleted;
        }
    }

    addTodo(ev) {

        if (ev.keyCode === 13 ) {

            const description = ev.target.value.trim();

            if (description !== "") {
                this.todos.push({
                    id: this.nextId++,
                    description,
                    isCompleted: false,
                });

                ev.target.value = "";

            }
        }
    }

    removeTodo(todoId) {
        const index = this.todos.findIndex((t) => t.id === todoId);
        if (index >= 0) {
            this.todos.splice(index, 1);
        }
    }
}
