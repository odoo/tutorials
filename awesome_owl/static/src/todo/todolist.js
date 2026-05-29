import { Component, useState } from "@odoo/owl";
import { useAutoFocus } from "../utils";
import { TodoItem } from "./todoitem";

export class TodoList extends Component {
    static template = "awesome_owl.TodoList";

    static components = { TodoItem };

    setup() {
        this.todos = useState([]);
        this.nextId = 1;
        this.inputRef = useAutoFocus('input');
    }

    addTodo(ev) {
        if (ev.key === "Enter") {
            const content = ev.target.value.trim();
            if (content !== "") {
                this.todos.push({ id: this.nextId, description: content, isCompleted: false });
                ev.target.value = "";
                this.nextId++;
            }
        }
    }

    toggleTodo(id) {
        const todo = this.todos.find(t => t.id === id);
        if (todo) {
            todo.isCompleted = !todo.isCompleted;
        }
    }

    deleteTodo(id) {
        const index = this.todos.findIndex((t) => t.id === id);
        if (index >= 0) {
            this.todos.splice(index, 1);
        }
    }
}
