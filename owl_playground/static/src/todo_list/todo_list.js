/** @odoo-module **/

import { Todo } from "../todo/todo";
import { Component, useState } from "@odoo/owl";
import { useAutofocus } from "../utils"

export class TodoList extends Component {
    setup() {
        this.nextId = 0;
        this.todoList = useState([]);
        useAutofocus("todoListInput"); //We use the useAutofocus hook to focus the input when the component is mounted
    }

    addTodo(ev) {
        if (ev.keyCode === 13 && ev.target.value != "") { //We check if the key pressed is the enter key and if the value is not empty
            this.todoList.push({ //We register the new todo in the todoList
                id: this.nextId++,
                description: ev.target.value,
                done: false,
            });
            ev.target.value = ""; //We reset the input value
        }
    }

    toggleTodo(todoId) {
        const todo = this.todoList.find(todo => todo.id === todoId); //We find the todo in the todoList
        if (todo) {
            todo.done = !todo.done; //We toggle the done property if the todo exists
        }
    }

    removeTodo(todoId) {
        const todo = this.todoList.find(todo => todo.id === todoId); //We find the todo in the todoList
        if (todo) {
            //eliminate the todo from the todoList
            const index = this.todoList.indexOf(todo);
            this.todoList.splice(index, 1);
        }
    }
}

TodoList.components = { Todo }
TodoList.template = "owl_playground.todo_list";