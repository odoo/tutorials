/** @odoo-module **/

import { Component, useState, useRef, onMounted } from "@odoo/owl";
import { TodoItem } from "./todo_item";
import { useFocus } from "../utils";
export class TodoList extends Component {
    static template = "awesome_owl.TodoList";
    setup() {
        this.todos = useState([]);
        this.todosCount = useState({ value: 0 });
        useFocus('input');
    }

    addTodo(ev) {
        if (ev.keyCode === 13 && ev.target.value){
            let nextId = this.todos.length + 1;
            this.todos.push({id: ++this.todosCount.value, description: ev.target.value, isCompleted: false});
            ev.target.value = "";
        } 
    }

    toggleTodo(todoId) {
        this.todos.forEach((todo) => {
            if (todo.id === todoId) {
                todo.isCompleted = !todo.isCompleted;
            }
        })
    }

    removeTodo(todoId) {
        // find the index of the element to delete
        const index = this.todos.findIndex((todo) => todo.id === todoId);
        if (index >= 0) {
            // remove the element at index from list
            this.todos.splice(index, 1);
        }
    }

    static components = { TodoItem };
}
