/** @odoo-module **/

import { Component, useState, useRef, onMounted } from "@odoo/owl";
import { useAutofocus } from "../utils"
import { TodoItem } from "./todo_item";

export class TodoList extends Component {
    static template = "awesome_owl.todo_list";
    static props = {};
    static components = { TodoItem };

    setup() {
        this.nextId = 0;
        this.todos = useState([]);

        useAutofocus('add-todo-input')
    }

    addTodo(event) {
        if (event.keyCode != 13 || event.target.value == '') return;

        this.todos.push({ id: this.nextId, description: event.target.value, isCompleted: false })

        event.target.value = ''
        this.nextId++;
    }

    toggleState(id) {
        const index = this.todos.findIndex((todo) => todo.id === id);
        if (index >= 0) {
            this.todos[index].isCompleted = !this.todos[index].isCompleted;
        }
    }

    removeTodo(id) {
        const index = this.todos.findIndex((todo) => todo.id === id);
        if (index >= 0) {
            this.todos.splice(index, 1);
        }
    }
}
