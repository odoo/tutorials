import { Component, useState, useRef } from "@odoo/owl";
import { TodoItem } from "./todo_item";
import { useAutofocus } from "../utils";

export class TodoList extends Component {
    static template = "awesome_owl.TodoList";
    static components = { TodoItem };

    setup() {
        this.todos = useState([])
        this.id = 1
        this.inputRef = useRef("input");
        useAutofocus(this.inputRef);
        this.removeTodo = this.removeTodo.bind(this)
    }

    addTodo(e){
        if (e.keyCode === 13 && e.target.value.trim()) {
            this.todos.push({
                id: this.id++,
                description: e.target.value,
                isCompleted: false
            });
            e.target.value = "";
        }
    }

    toggleState(id) {
        const todo = this.todos.find(todo => todo.id === id)
        todo.isCompleted = !todo.isCompleted
    }

    removeTodo(id) {
        this.todos.splice(this.todos.findIndex((todo) => todo.id === id), 1)
    }
}
