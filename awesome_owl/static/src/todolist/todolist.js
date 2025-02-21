/** @odoo-module **/
import { Component, onMounted, useState, useRef } from "@odoo/owl";
import { TodoItem } from "./todoitem";
import { useAutofocus } from "../utils";

export class TodoList extends Component {
    static template = "awesome_owl.TodoList";
    static components = { TodoItem };

    setup() {
        this.todos = useState([]);
        this.nextId = 1;
        useAutofocus("input");
        this.toggleState = (todoId) => {
            const todo = this.todos.find((t) => t.id === todoId);
            if (todo) {
                todo.isCompleted = !todo.isCompleted;
            }
        };
        this.removeTodo = (todoId) =>  {
            const index = this.todos.findIndex((t) => t.id === todoId);
            if (index !== -1) {
                this.todos.splice(index, 1);
            }
        }
    }

    addTodo(ev) {
        if (ev.keyCode === 13 && ev.target.value.trim()) { 
                this.todos.push({ id: this.nextId++, description: ev.target.value.trim(), isCompleted: false });
                ev.target.value = "";
        }
    }
}
