/** @odoo-module **/

import { Component, useState, useRef, onMounted } from "@odoo/owl";
import { TodoItem } from "../todo_item/todo_item";
import { useAutofocus } from "../utils/autofocus";

export class TodoList extends Component {
    static template = "awesome_owl.todo_list";
    static components = { TodoItem };

    setup() {
        this.id = 0;
        this.todos = useState([]);
        useAutofocus("ref_todo_input");
    }

    addTodo(ev){
        if(ev.keyCode === 13 && ev.target.value !== "") {
            this.id++;
            this.todos.push({id: this.id, description: ev.target.value, isCompleted: false});
            ev.target.value = "";
        }
    }

    toggleTodoCompleted(todoId) {
        const todo = this.todos.find(t => t.id === todoId);
        if (todo) {
            todo.isCompleted = !todo.isCompleted;
        }
    }
}