/** @odoo-module **/

import {Component, useState, useRef, onMounted} from "@odoo/owl";
import {ToDoItem} from "./to_do_item";

export class ToDoList extends Component {
    static template = "awesome_owl.todolist";

    setup() {
        this.todos = useState([]);
        this.myRef = useRef("refInput")
        onMounted(() => {
            this.myRef.el.focus();
        });
    }

    addToDo(ev) {
        if (ev.keyCode === 13 && ev.target.value !== "") {
            this.todos.push({id: this.todos.length, description: ev.target.value, isCompleted: false})
            ev.target.value = ""
        }
    }

    toggleState(ev) {
        const todo = this.todos.find(todo => todo.id === parseInt(ev.target.id));
        todo.isCompleted = !todo.isCompleted;
    }

    removeTodo(todoId) {
        const todoIndex = this.todos.findIndex((todo) => todo.id === todoId);
        if (todoIndex >= 0) {
            this.todos.splice(todoIndex, 1);
        }
    }

    static components = {ToDoItem}
}
