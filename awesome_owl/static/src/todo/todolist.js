import { Component, useState } from "@odoo/owl"
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
    static components = { TodoItem }
}
