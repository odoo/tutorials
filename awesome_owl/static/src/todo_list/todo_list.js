/** @odoo-module **/

import { Component, useState } from "@odoo/owl"
import { useAutofocus } from "./utils";
import { TodoItem } from "./todo_item";

export class TodoList extends Component {
    static template = "awesome_owl.TodoList";
    static components = { TodoItem }
    
    setup(){
        this.todos = useState([]);
        this.counter = useState({ value: 0 });
        useAutofocus("input");
        this.toggleState = (id) => {
            const todo = this.todos.find(todo => todo.id === id);
            if (todo) {
                todo.isCompleted = !todo.isCompleted;
            }
            console.log(this.todos)
        }
    }

    addTodo(ev) {
        if (ev.keyCode === 13 && ev.target.value != "") {
            this.counter.value++;
            this.todos.push({ id: this.counter.value, description: ev.target.value, isCompleted: false });
            ev.target.value = "";
        }
    }

    toggleState = (id) => {
        const todo = this.todos.find(todo => todo.id === id);
        if (todo) {
            todo.isCompleted = !todo.isCompleted;
        }
    }
    
    removeTodo = (todoId) => {
        const index = this.todos.findIndex((todo) => todo.id === todoId);
        if (index >= 0) {
            this.todos.splice(index, 1);
        }
    }
}
