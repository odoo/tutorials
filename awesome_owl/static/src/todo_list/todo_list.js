/** @odoo-module **/

import { Component, onMounted, useRef, useState } from "@odoo/owl";
import { TodoItem } from "../todo_item/todo_item";
// import { useAutofocus } from "../util";

export class TodoList extends Component {
    static template = "awesome_owl.todo_list";
    static components = { TodoItem };

    setup() {
        this.nextId = 4;
        this.todos = useState([
            { id: 1, description: "Buy milk", isCompleted: false },
            { id: 2, description: "Walk the dog", isCompleted: true },
            { id: 3, description: "Do homework", isCompleted: false },
        ]);
        this.inputRef = useRef("input");
        onMounted(() => {
            this.inputRef.el.focus();
        });
        // useAutofocus(this.inputRef);
    }

    addTodo(e) {
        if (e.keyCode === 13) {
            const input = e.target;
            const description = input.value.trim();
            if (description) {
                this.nextId++;
                this.todos.push({ id: this.nextId, description, isCompleted: false });
                input.value = "";
            }
        }
    }

    markCompleted(id) {
        const todo = this.todos.find(t => t.id === id);
        if (todo) {
            todo.isCompleted = !todo.isCompleted;
        }
    }

    deleteTodo(id) {
        const index = this.todos.findIndex(todo => todo.id === id);
        if (index >= 0) {
            this.todos.splice(index, 1);
        }
    }
}
