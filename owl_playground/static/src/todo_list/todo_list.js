/** @odoo-module */

import { Todo } from "../todo/todo";
import { useAutofocus } from "../utils";

import { Component, useState } from "@odoo/owl";

export class TodoList extends Component {
    static template = "owl_playground.todoList";
    setup() {
        this.nextId = 1;
        this.todoList = useState([]);
        useAutofocus("todoListInput");
    }

    addTodo(ev){
        if (ev.keyCode === 13  && ev.target.value != "") {
            this.todoList.push({
                id: this.nextId++,
                description: ev.target.value,
                done : false,
            });

            ev.target.value = "";
        }
    }

    toggleTodo(todoId) {
        const todo = this.todoList.find((todo) => todo.id === todoId);
        if (todo) {
            todo.done = !todo.done;
        }
    }

    removeTodo(elemId){
        const index = this.todoList.findIndex((elem) => elem.id === elemId);
        if (index >= 0) {
            this.todoList.splice(index, 1);
        }
    }

    static components = { Todo };
}

