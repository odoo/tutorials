/** @odoo-module **/

import { Component, useState, useRef, onMounted } from "@odoo/owl";
import { TodoItem } from "./todo_item";
import { useAutofocus } from "../utils";
import { Counter } from "../counter/counter";


export class TodoList extends Component {
    static template = "awesome_owl.todo_list";
    static components = { TodoItem, Counter };

    setup() {
        this.todos = useState([]);
        this.nextId = 1;
        this.inputRef = useRef('input');
        this.toggleTodoState = this.toggleTodoState.bind(this);
        this.removeTodo = this.removeTodo.bind(this);

        // Focuse the input when the component is mounted
        onMounted(() => {
            this.inputRef.el.focus();
        });

        // Use the useAutofocus hook to focus the input
        // this.inputRef = useAutofocus('input');
    }

    toggleTodoState(todoId){
        const todo = this.todos.find((t)=> t.id === todoId);
        if(todo){
            todo.isCompleted = !todo.isCompleted;
        }
    }
    removeTodo(todoId) {
        const index = this.todos.findIndex((t) => t.id === todoId);
        if (index >= 0) {
            this.todos.splice(index, 1); 
        }
    }
    addTodo(ev) {
        if (ev.keyCode === 13) {
            let input = ev.target;
            let description = input.value.trim();
            if (description !== "") {
                this.todos.push({
                    id: this.nextId++,
                    description: description,
                    isCompleted: false,
                });
                input.value = ""; 
            }
        }
    }
}
