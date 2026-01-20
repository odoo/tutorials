import { Component, useState } from "@odoo/owl";
import { useAutofocus } from "../utils";
import { TodoItem } from "./todo_item";

export class TodoList extends Component {
    static template = "awesome_owl.TodoList";
    static components = {TodoItem};

    setup() {
        this.idCounter = 0;
        this.todos = useState([]);
        useAutofocus("input");
        this.toggleState = this.toggleState.bind(this);
        this.deleteTodo = this.deleteTodo.bind(this);
    }

    addTodo(ev) {
        if (ev.keyCode === 13 && ev.target.value != "") {
            this.todos.push({
                id: this.idCounter++,
                description: ev.target.value,
                isCompleted: false
            });
            ev.target.value = "";
        }
    }

    toggleState(id) {
        const todo = this.todos.find((t) => t.id === id);
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
