import { Component, useState } from "@odoo/owl";
import { TodoItem } from "./todoitem";
import { useAutoFocus } from "../utils"

export class TodoList extends Component {
    static template = "awesome_owl.TodoList";
    static components = { TodoItem }

    setup() {
        this.todos = useState([])
        this.nextId = 0
        useAutoFocus('todoitem_input')
    }

    addTodo(e) {
        if (e.keyCode === 13 && e.target.value != "") {
            this.todos.push({
                id: this.nextId++,
                description: e.target.value,
                isCompleted: false
            })
        }
    }

    toggleTodo(todoId) {
        const todo = this.todos.find((todo) => todo.id === todoId);
        if (todo) {
            todo.isCompleted = !todo.isCompleted;
        }
    }

    removeTodo(todoId) {
        const todoInd = this.todos.findIndex((todo) => todo.id === todoId);
        if (todoInd >= 0) {
            this.todos.splice(todoInd, 1)
        }
    }
}
