/** @odoo-module **/

import { Component, useState, useRef, onMounted } from "@odoo/owl";
import { TodoItem } from "./todo_item";
import { Todo } from "./todo";
import { useAutoFocus } from "../utils";

export class TodoList extends Component {
    static template = "awesome_owl.todolist";
    static components = { TodoItem };

    setup() {
        this.todos = useState([]);
        useAutoFocus("input");
    }

    addTodo(ev) {
        if (ev.keyCode === 13 && ev.target.value !== '') {
            this.todos.push(new Todo(ev.target.value))
            ev.target.value='';
        }
    }

    removeTodo(id) {
        const index = this.todos.findIndex((elem) => elem.id === id);

        if (index >= 0) {
            this.todos.splice(index, 1);
        }  
    }
}
