import { Component, useState } from "@odoo/owl";
import { TodoItem } from "./todo_item";
import { useAutofocus } from './../utils'


export class TodoList extends Component {
    static template = "awesome_owl.TodoList";
    static props = {};
    static components = { TodoItem };

    setup() {
        this.todos = useState([])
        useAutofocus('todoInputRef')
    }

    addTodo(ev) {
        if(ev.keyCode == '13') {
            if(ev.target.value != ""){
                this.todos.push({
                    id: this.todos.length + 1,
                    description: ev.target.value,
                    isCompleted: false
                })
                ev.target.value = ''
            }
        }
    }

    toggleState(id) {
        const todo = this.todos.find(todo => todo.id == id)
        todo.isCompleted = !todo.isCompleted
    }

    deleteTodo(id) {
        const index = this.todos.findIndex(todo => todo.id === id)
        if (index >= 0){
            this.todos.splice(index, 1)
        }
    }
}
