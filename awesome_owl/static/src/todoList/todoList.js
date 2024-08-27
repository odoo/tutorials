/** @odoo-module **/

import {Component, onMounted, useRef, useState} from "@odoo/owl";
import {TodoItem} from "./todoItem";

export class TodoList extends Component {
    static template = "awesome_owl.todoList";
    static components = {TodoItem};

    setup() {
        this.todos = useState([]);
        this.todoInputRef = useRef("todoInput")
        onMounted(() => {
            this.todoInputRef.el.focus()
        })
    }

    addTodo(ev) {
        if (ev.keyCode === 13) {
            let todoInput = this.todoInputRef.el
            this.todos.push({id: this.findFirstIndex(), description: todoInput.value, isCompleted: false});
            todoInput.value = "";
        }
    }

    findFirstIndex() {
        let ids = this.todos.map(todo => todo.id)
        for (let i = 0; i < this.todos.length + 1; i++) {
            // this.todos.length + 1 to make sure to return an index <=> "return this.todos.length" outside the loop
            if (!ids.includes(i)) {
                return i;
            }
        }
    }

    toggleState(id) {
        const todo = this.todos.find((todo) => todo.id === id);
        if (todo) {
            todo.isCompleted = !todo.isCompleted
        }
    }

    removeState(id) {
        const index = this.todos.findIndex((elem) => elem.id === id)
        this.todos.splice(index, 1)
    }
}
