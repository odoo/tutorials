import { Component , useState, useRef, onMounted } from "@odoo/owl"
import { TodoItem } from "./todoitem"
import { useAutoFocus } from "../utils"

export class TodoList extends Component{
    static template = "awesome_owl.todo_list"

    setup(){
        this.todos = useState([])
        this.counter = useState({value:1})
        useAutoFocus("inputTodo")
    }

    addTodo(event){
        if(event.keyCode == 13 && event.target.value.trim()){
            this.todos.push({ 'id': this.counter.value++ ,'description': event.target.value, 'isCompleted': false })
            event.target.value = ""
        }
    }

    toggleState(todoItemId){
        const todo = this.todos.find(todo => todo.id === todoItemId)
        if(todo){
            todo.isCompleted = !todo.isCompleted
        }
    }

    removeTodo(todoItemId){
        const index = this.todos.findIndex(todo => todo.id === todoItemId)
        if(index > 0){
            this.todos.splice(index,1)
        }
    }

    static components = { TodoItem }
}
