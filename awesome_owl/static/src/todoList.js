/** @odoo-module **/

import { Component, useState, useRef } from "@odoo/owl";
import { TodoItem } from "./todoItem";


export class TodoList extends Component {
    static template = "awesome_owl.todoList";

    setup() {
        this.newTaskName = useRef("newTaskName");
        this.state = useState({ todos: [], nextId: 0 });

    }

    addTodo(ev) {
        if (ev.keyCode === 13) {
            this.createTodo();
        }
    }

    createTodo() {
        this.state.nextId++;
        this.state.todos.push({
            id: this.state.nextId,
            description: this.newTaskName.el.value,
            isCompleted: false,
        });
        this.newTaskName.el.value = "";
    }

    toggleState(ev, id){
        this.state.todos.forEach(todo => {
            if (todo.id === id){
                todo.isCompleted = ev.target.checked;
            }
        });
    }

    removeTodo(ev, id){
        const index = this.state.todos.findIndex((todo) => todo.id === id);
        if (index >= 0) { this.state.todos.splice(index, 1); }
    }

    static components = { TodoItem };

}