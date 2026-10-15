import {TodoItem} from "./TodoItem"
import {Component, useState} from "@odoo/owl";

export class TodoList extends Component {
    static template = "awesome_owl.TodoList";
    static components = {TodoItem}

    setup() {
        this.todos = useState([])
    }

    addTodo(e) {
        if (e.keyCode === 13) {
            if (e.target.value) {
                this.todos.push({
                    id: this.todos.length + 1, description: e.target.value.trim(), isCompleted: false
                })
                e.target.value = ''
            }
        }
    }
}
