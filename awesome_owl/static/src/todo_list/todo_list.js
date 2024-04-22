/** @odoo-module **/

import { Component, useState, onMounted, useRef } from "@odoo/owl";
import {TodoItem} from "./todo_item";

export class TodoList extends Component {
    static template = "awesome_owl.todo_list";
    static components = { TodoItem };
    
    setup() {
        this.nextId = 0;
        this.todos = useState([]);
        this.inputRef = useRef('input');
        onMounted(() => {
            this.inputRef.el.focus();
         });
    }

    addTodo(ev) {
        if(ev.keyCode === 13 && ev.target.value) {
            this.todos.push({'id': this.nextId, 'description': ev.target.value, 'isCompleted': false})
            ev.target.value = "";
            this.nextId++;
        }
    }

    toggleState(id) {
        const index = this.todos.findIndex((elem) => elem.id === id);
        if (index >= 0) {
            this.todos[index].isCompleted  =  !this.todos[index].isCompleted;
        }
    }

    removeTodo(id) {
        const index = this.todos.findIndex((elem) => elem.id === id);
        if (index >= 0) {
        this.todos.splice(index, 1);
        }
    }
}