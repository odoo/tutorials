import { Component, useState } from "@odoo/owl";
import { TodoItem } from "./todo_item";
import { useAutoFocus } from "../hooks";

export class TodoList extends Component {
    static template = "awesome_owl.todo_list";
    static components = { TodoItem };
    static props = [];

    setup() {
        this.nextId = 1;
        this.todos = useState([]);
        useAutoFocus('input');
    }

    addTodo(e) {
        if (e.keyCode !== 13) return;

        const input = e.target.value
        if (!input) return

        this.todos.push({
            id: this.nextId++,
            description: input,
            isCompleted: false,
        })

        e.target.value = "";
    }

    toggleCompleted(id) {
        const todo = this.todos.find(todo => todo.id === id);
        todo.isCompleted = !todo.isCompleted;
    }

    removeTodo(id) {
        const index = this.todos.findIndex(todo => todo.id === id);
        this.todos.splice(index, 1);
    }
}
