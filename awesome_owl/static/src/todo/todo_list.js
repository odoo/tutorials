/** @odoo-module **/

import { Component, useState, useRef, onMounted } from "@odoo/owl";

import { TodoItem } from "./todo_item.js"

export class TodoList extends Component {

    static template = "awesome_owl.TodoList";
    static components = { TodoItem };

    setup() {
        this.todos = useState([]);
        this.taskCounter = 0;

        this.inputTodoRef = useRef("addTodoInput");
        onMounted(() => { this.inputTodoRef.el.focus(); });
    }

    addTodo(ev) {
        if (ev.keyCode != 13 || ev.srcElement.value === "")
            return;

        this.todos.push({ id: this.taskCounter, description: this.inputTodoRef.el.value, isCompleted: false });
        this.inputTodoRef.el.value = "";
        this.taskCounter++;
    }

    toggleComplete(todo_item_id) {
        this.todos
            .filter(todo_item => todo_item.id === todo_item_id)
            .forEach(todo_item => { todo_item.isCompleted = !todo_item.isCompleted });
    }
}