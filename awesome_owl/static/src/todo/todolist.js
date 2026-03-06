import { Component, useState } from "@odoo/owl";
import { TodoItem } from "./todoitem";
import { useAutofocus } from "../utils";

export class TodoList extends Component {
    static template = "awesome_owl.todolist";
    static components = { TodoItem };

    setup() {
        this.nextId = 0;
        this.todos = useState([]);
        // autofocus hook
        this.inputRef = useAutofocus("todo_input");
    }

    addTodo(ev) {
        if (ev.keyCode === 13) {
            const description = ev.target.value.trim();
            if (!description) {
                return;
            }
            this.todos.push({
                id: this.nextId++,
                description: description,
                isCompleted: false,
            });
            ev.target.value = "";
        }
    }

    toggleState(id) {
        const todo = this.todos.find(t => t.id === id);
        if (todo) {
            todo.isCompleted = !todo.isCompleted;
        }
    }
}
