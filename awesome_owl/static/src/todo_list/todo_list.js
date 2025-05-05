/** @odoo-module **/

import { Component, useState, onMounted, useRef } from "@odoo/owl";
import { TodoItem } from "./todo_item";

export class TodoList extends Component {
    static template = "awesome_owl.todo_list";
    static components = { TodoItem };

    todos = useState([]);
    state = useState({ count: 0 });

    setup() {
        this.inputRef = useRef("input");

        onMounted(() => {
            if (this.inputRef.el) {
                this.inputRef.el.focus();
            }
        });
    }


    addTodo(ev) {
        if (ev.key === 'Enter' && ev.target.value) {
            const newTodo = {
                id: this.state.count = this.state.count + 1,
                description: ev.target.value,
                isCompleted: false,
            };
            this.todos.push(newTodo);
            ev.target.value = "";
        }
    }

    toggleTodoCompleted(todoId) {
        this.todos.forEach(todo => {
            if (todo.id === todoId) {
                todo.isCompleted = !todo.isCompleted;
            }
        });
    }
}
