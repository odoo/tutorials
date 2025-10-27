/** @odoo-module **/

import { Component, useState, useRef, onMounted } from "@odoo/owl";
import { TodoItem } from "./todo_item";

export class TodoList extends Component {
    static template = "awesome_owl.todo_list";

    
    setup() {
        this.todos = useState([]);
        this.inputRef = useRef('todoInput');
        onMounted(() => {
            if (this.inputRef.el) {
                this.inputRef.el.focus();
            }
        });
    }

    addTodo(ev) {
        // event.Key === "Enter" marche aussi
        if (ev.keyCode === 13 && ev.target.value.trim() != "") {
            this.todos.push({id: this.todos.length + 1, description: ev.target.value, isCompleted: false});
            ev.target.value = ""
        }
    }

    removeTodo(id) {
        const index = this.todos.findIndex(todo => todo.id === id);
        if (index >= 0) {
            this.todos.splice(index, 1);
        }
    }

    static components = { TodoItem }
}
