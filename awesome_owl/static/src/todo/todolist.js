import { Component, useState } from "@odoo/owl";
import { TodoItem } from "./todoitem";
import { useAutofocus } from "../utils";


export class TodoList extends Component {
    static template = "awesome_owl.todolist";
    static components = { TodoItem };

    setup() {
        this.todos = useState([])
        useAutofocus("todo_input")
    }

    addTodo(ev) {
        if (ev.keyCode == '13') {   
            if (ev.target.value != ""){
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
        todo.isCompleted = !todo.isCompleted;
    }

    removeTodo(id){
        const index = this.todos.findIndex((elem) => elem.id === id);
        if (index >= 0){
            this.todos.splice(index,1)
        }
    }
}
