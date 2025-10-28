import { Component, useState, useRef, onMounted } from "@odoo/owl"
import { TodoItem } from "./item"
import { useAutofocus } from './../utils'


export class TodoList extends Component {
    static template = "awesome_owl.todo.list"
    static components = {TodoItem}

    setup() {
        this.todos = useState([])
        useAutofocus('todoInputRef')
    }
    addTodo(ev) {
        if(ev.keyCode == '13' && ev.target.value != '') {
            this.todos.push({
                id: this.todos.length + 1,
                description: ev.target.value,
                isCompleted: false
            })
            ev.target.value = ''
        }
    }
    toggleState(id) {
        const [res] = this.todos.filter(todo => todo.id == id)
        res.isCompleted = true
        
    }
    deleteTodo(id) {
        const [res] = this.todos.filter(todo => todo.id == id)
        this.todos.splice(this.todos.indexOf(res), 1)
    }
}
