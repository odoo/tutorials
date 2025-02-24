import { Component, useState } from "@odoo/owl";

import { TodoItem } from "./todoItem/todoItem";

export class TodoList extends Component {
    static template = "awesome_owl.todo.list";
    static components = { TodoItem };

    setup() {
        this.todos = useState([]);
        this.newTodo = useState({ newDescription : "", nextId : 1});
    }

    addTodo(ev) {
        if (ev.keyCode === 13 && this.newTodo.newDescription.trim()) {
            this.todos.push({ id: this.newTodo.nextId, description : this.newTodo.newDescription, isCompleted : false });
            this.newTodo.nextId++;
            this.newTodo.newDescription = "";
        }
    }
}