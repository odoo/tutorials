import { Component, useState } from "@odoo/owl";
import { TodoItem } from "./todo_item";
import { useAutofocus } from "../utils";

export class TodoList extends Component {
    static template = "awesome_owl.todolist";
    static components = { TodoItem };

    setup() {
        this.state = useState({todos : []});
        useAutofocus("input");
    }

    addTodo(ev) {
        if (ev.keyCode === 13 && ev.target.value.trim().length > 0) {
            this.state.todos.push({ id: this.state.todos.length, description: ev.target.value.trim() });
            ev.target.value = "";
        }
    }

    removeTodo(todo) {
        const index = this.state.todos.findIndex(t => t.id === todo.id);
        if (index !== -1) {
            this.state.todos.splice(index, 1);
        }
    }

    toggle(todo) {
        todo.isCompleted = !todo.isCompleted;
    }
}
