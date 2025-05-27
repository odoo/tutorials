/** @odoo-module **/

import { Component, useState, useRef, onMounted } from "@odoo/owl";
import { TodoItem } from "./todo_item.js";

export class TodoList extends Component {
    static template = "awesome_owl.todo_list";
    static components = { TodoItem };

    lastId = 1;

    setup() {
        this.todos = useState([]);
        this.inputRef = useRef("todo_input");
        onMounted(() => {
            this.inputRef.el.focus();
        });
    }

    addTodo(event) {
        const enterKeycode = 13;
        if(event.keyCode !== enterKeycode || event.target.value == '') {
            return;
        }

        let newTodo = {
            id: this.lastId++,
            description: event.target.value,
            isCompleted: false
        };

        this.todos.push(newTodo);
        event.target.value = '';
    }

    removeFromList(todoId) {
        let index = this.todos.findIndex(todo => todo.id === todoId);
        if(index > -1) {
            this.todos.splice(index, 1);
        }
    }
}
