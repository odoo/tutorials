/** @odoo-module **/

import { Component, onMounted, useRef, useState } from "@odoo/owl";
import { TodoItem } from "./todo_item";
import { useAutofocus } from "../utils";

export class TodoList extends Component {
    static template = "awesome_owl.todo_list";
    static components = { TodoItem };

    setup() {
        this.todos = useState([]);
        this.todoCounter = useState({ value: 1 });
        useAutofocus('todo_input');
        // this.inputRef = useRef('todo_input');
        // onMounted(() => {
        //     this.inputRef.el.focus();
        // })
    }

    addTodo(e) {
        if (e.keyCode === 13 && e.target.value) {
            this.todos.push({
                id: this.todoCounter.value,
                description: e.target.value,
                isCompleted: false
            });
            this.todoCounter.value++;
            e.target.value = '';
        }
    }

    updateState(id) {
        this.todos.forEach(todo => (todo.id === id 
            ? (todo.isCompleted = !todo.isCompleted) 
            : todo))
    }
}
