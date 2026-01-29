import { Component, useState, useRef, onMounted } from "@odoo/owl";
import { TodoItem } from "./todo_item";
import { useAutofocus } from "../utils.js";

export class TodoList extends Component {
    static template = "awesome_owl.todo_list";
    static components = { TodoItem };

    setup() {
        this.todos = useState([]);
        this.nextId = 1;
        useAutofocus("input");
    }

    addTodo(ev) {
        if (ev.keyCode === 13) {
            const input = ev.target;
            const description = input.value.trim();
            
            if (description) {
                this.todos.push({
                    id: this.nextId++,
                    description: description,
                    isCompleted: false
                });
                input.value = "";
            }
        }
    }

    toggleState(todoId) {
        const todo = this.todos.find(t => t.id === todoId);
        if (todo) {
            todo.isCompleted = !todo.isCompleted;
        }
    }

    removeTodo(todoId) {
        const index = this.todos.findIndex(t => t.id === todoId);
        if (index !== -1) {
            this.todos.splice(index, 1);
        }
    }
}
