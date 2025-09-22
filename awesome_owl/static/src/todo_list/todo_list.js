/** @odoo-module **/

import { Component, useState } from "@odoo/owl";
import { TodoItem } from "./todo_item";
import { Todo } from "./todo";
import { useAutofocus } from "../utils";

export class TodoList extends Component {
    static template = "awesome_owl.TodoList";
    static components = { TodoItem };

    setup() {
        this.todos = useState([]);
        this.sequence = 0;
        useAutofocus("new-todo");
    }

    addTodo(event) {
        if (event.keyCode === 13 && event.target.value.trim() !== "") {
            this.sequence++;
            this.todos.push(new Todo(this.sequence, event.target.value));
            event.target.value = "";
        }
    }

    toggleState(id) {
        const todo = this.todos.find(t => t.id === id);
        if (todo) todo.setIsCompleted(!todo.isCompleted);
    }

    removeTodo(id) {
        const index = this.todos.findIndex((elem) => elem.id === id);
        if (index !== -1) this.todos.splice(index, 1);
    }
}
