/** @odoo-module **/

import { Component, useState } from "@odoo/owl";
import { TodoItem } from "./todo_item";
import { useAutofocus } from "../utils";

export class TodoList extends Component {
    static template = "awesome_owl.todo_list";
    static components = { TodoItem }

    setup() {
        this.todos = useState([]);
        this.nextId = 1;
        useAutofocus("todoInput");
    }

    addTodo(ev) {
        if(ev.keyCode === 13) {
            var input = ev.target;
            var description = input.value.trim();
            if(description) {
                this.todos.push({id: this.nextId++, description, isCompleted: false});
                input.value = '';
            }
        }
    }

    toggleState(id) {   
        this.todos.forEach(todo => {
            if(todo.id === id) {
                todo.isCompleted = !todo.isCompleted
            }
        });
    }

    removeTodo(todoId) {
        var index = this.todos.findIndex((todo) => todo.id === todoId);
        if (index >= 0) {
            this.todos.splice(index, 1);
        }
    }
}
