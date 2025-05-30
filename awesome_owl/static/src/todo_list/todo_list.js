import {Component, useState} from "@odoo/owl";
import {TodoItem} from "./todo_item";
import { useAutofocus } from "../utils";

export class TodoList extends Component {
    static template = "awesome_owl.TodoList";
    static components = {TodoItem};

    setup() {
        this.todos = useState([]);
        useAutofocus("input")
    }

    addTodo(ev) {
        if (ev.keyCode === 13 && ev.target.value.trim() != "") {
            const newTodo = {
                id: this.todos.length + 1,
                description: ev.target.value.trim(),
                isCompleted: false,
            };
            this.todos.push(newTodo);
            ev.target.value = "";
        }
    }
    toggleTodo(id) {
        const todo = this.todos.find(todo => todo.id === id);
        if (todo) {
            todo.isCompleted = !todo.isCompleted;
        }
    }

    removeTodo(id) {
        const index = this.todos.findIndex(todo => todo.id === id);
        if (index !== -1) {
            this.todos.splice(index, 1);
        }
    }
}