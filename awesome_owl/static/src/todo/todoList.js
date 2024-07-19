/** @odoo-module **/

import { Component, useState, useRef, onMounted } from "@odoo/owl";
import { TodoItem } from "./todoItem";

export class TodoList extends Component {
    static template = "awesome_owl.todo_list";
    static components = { TodoItem };

    setup() {
        this.todos = useState([]);
        this.inputRef = useRef("todo-input");

        onMounted(() => {
            this.inputRef.el.focus();
        });
    }

    addTodo(event) {
        if (event.keyCode === 13 && event.target.value != "") {
            let newId = 0;
            if (this.todos.length) {
                newId = this.todos[this.todos.length - 1].id + 1;
            }
            this.todos.push({
                id: newId,
                description: event.target.value,
                isCompleted: false,
            });
            event.target.value = "";
        }
    }

    toggleTodo(id) {
        const todo = this.todos.find((todo) => todo.id === id);
        if (todo) {
            todo.isCompleted = !todo.isCompleted;
        }
    }

    removeTodo(id) {
        const todoIndex = this.todos.findIndex((todo) => todo.id === id);
        if (todoIndex >= 0) {
            this.todos.splice(todoIndex, 1);
        }
    }
}
