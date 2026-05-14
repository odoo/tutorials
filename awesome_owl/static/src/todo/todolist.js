import { Component, useState, useRef } from "@odoo/owl"
import { TodoItem } from "./todoitem"
import { useAutofocus } from "../utils"


export class TodoList extends Component {
    static template = 'awesome_owl.TodoList'

    setup() {
        useAutofocus('input')
        this.todos = useState([])
        this.id = 1
    }

    addTodo(event) {
        if (event.keyCode == 13 && event.target.value != "") {
            this.todos.push({ id: this.id, description: event.target.value, isCompleted: false })
            this.id++
            event.target.value = ""
        }
    }

    toggleTodo(todoId) {
        const todo = this.todos.find((Todo) => Todo.id == todoId)
        if (todo) {
            todo.isCompleted = !todo.isCompleted
        }
    }

    deleteTodo(todoId) {
        const index = this.todos.findIndex((todo) => todo.id === todoId)
        if (index >= 0) {
            this.todos.splice(index, 1)
        }

    }

    static components = { TodoItem }
}
