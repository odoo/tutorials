/** @odoo-module */

import { Component, useState, useRef } from '@odoo/owl';
import { TodoItem } from './todo_item.js';

export class TodoList extends Component {
    static template = "awesome_owl.TodoList";
    static components = { TodoItem };

    setup() {
        this.todos = useState([]);
        this.nextId = 1; 
        this.inputRef = useRef('todoInput'); 
    }

    addTodo(ev) {
        if (ev.keyCode === 13) {  
            const newTodo = this.inputRef.el.value.trim();
            if (newTodo) {
                this.todos.push({ id: this.nextId++, description: newTodo, isCompleted: false });
                this.inputRef.el.value = '';  
            }
        }
    }
}
