/** @odoo-module **/

import { Component, useState, onMounted, useRef } from "@odoo/owl";
import { TodoItem } from "./todo_item";

export class TodoList extends Component {
    static template = "awesome_owl.todo_list";
    static components = { TodoItem };


    setup() {
        this.inputRef = useRef("input");
        this.todos = useState(new Array());
        this.state = useState({ count: 0 });

        onMounted(() => {
            if (this.inputRef.el) {
                this.inputRef.el.focus();
            }
        });
    }


    addTodo(ev) {
        if (ev.key === 'Enter' && ev.target.value) {
            const newTodo = {
                id: this.state.count,
                description: ev.target.value,
                isCompleted: false,
            };
            this.todos.push(newTodo);
            ev.target.value = "";
            this.state.count++;
        }
    }

    toggleTodo(todoId) {
        for (let todo of this.todos) {
            if (todo.id === todoId) {
                todo.isCompleted = !todo.isCompleted;
            }
        }
    }

    removeTodo(todoId) {
        const index = this.todos.findIndex((elem) => elem.id === todoId);
        if (index >= 0) {
            this.todos.splice(index, 1);
        }
    }
}
