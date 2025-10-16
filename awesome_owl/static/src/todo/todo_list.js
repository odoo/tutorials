/** @odoo-module **/

import { Component, useState, useRef } from "@odoo/owl";
import { TodoItem } from './todo_item'

export class Todolist extends Component {
    static components = {TodoItem};
    static template = "awesome_owl.todo_list";

    setup() {
        this.state = useState({idCounter: 1, todoItems: []})
        this.inputRef = useRef('input');
    }

    addTodo(ev) {
        if (ev.keyCode === 13 && ev.target.value) {
            let newTodoItem = {id: this.state.idCounter++, description: ev.target.value, isCompleted: false}
            this.state.todoItems = [...this.state.todoItems, newTodoItem];
        }
    }

    inputFocus() {
        this.inputRef.el.focus()
    }

    onStatusChange(id) {
        const todoItemToToggle = this.state.todoItems.find(obj => obj.id === id);
        todoItemToToggle.isCompleted = !todoItemToToggle.isCompleted;
    }

    deleteTodoItem(id) {
        this.state.todoItems = this.state.todoItems.filter(obj => obj.id !== id);
    }
}
