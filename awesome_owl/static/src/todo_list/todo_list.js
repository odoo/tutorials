/** @odoo-module **/

const { Component, useState, useRef, useEffect } = owl;
import { TodoItem } from "./todo_item";
import { useAutofocus } from "../utils";

export class TodoList extends Component {
    static template = "awesome_owl.todo_list";


    setup() {
        this.todos = useState([]);
        this.counter = useState({ value: 1 })
        useAutofocus('todo_input');
    }

    static components = { TodoItem }

    addTodo(ev) {
        if (ev.keyCode === 13 && ev.target.value !== "") {
            let todo = {
                id: this.counter.value,
                description: ev.target.value,
                isCompleted: false
            }
            this.todos.push(todo);
            this.counter.value++;
        }
    }

    toggleState(target_id) {
        let todo = this.todos.find(todo => todo.id === target_id)
        if (todo) {
            todo.isCompleted = !todo.isCompleted;
        }
    }

    removeTodo(target_id) {
        let todo_index = this.todos.findIndex(todo => todo.id === target_id)
        if (todo_index >= 0) {
            console.log(this.todos.splice(todo_index, 1));
        }
    }

}

