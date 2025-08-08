import { Component, onMounted, useState, useRef } from "@odoo/owl";
import { TodoItem } from "./todoItem";
import { useAutofocus } from "./utils";
export class TodoList extends Component {
    static template = "awesome_owl.todoList";
    static components = { TodoItem };

    setup() {
        this.todos = useState([])
        this.todoId = 1
        useAutofocus('todo_input')
        this.toggleState = this.toggleState.bind(this)
        this.removeTodo = this.removeTodo.bind(this)
    }

    addTodo(ev) {
        if(ev.keyCode === 13 && ev.target.value != ""){
            this.todos.push({id: this.todoId++, description: ev.target.value, isCompleted: false})
        }
    }

    toggleState(id) {
        const todo = this.todos.find(item => item.id === id)
        todo.isCompleted = !todo.isCompleted
    }

    removeTodo(id) {
        this.todos.splice(this.todos.findIndex(item => item.id === id), 1)
    }

}