/** @odoo-module **/

import { Component, useState } from "@odoo/owl";
import { TodoItem } from "../todoitem/todoitem";
import { useAutofocus } from "../utils";


export class TodoList extends Component{
    static template = "awesome_owl.Todolist";
    setup(){
        this.id = 1
        this.todos = useState([]);
        // this.refs.inputTask.focus()
        useAutofocus("inputTask")
    }
    addTodo(ev){
        if (ev.keyCode === 13 && ev.target.value.trim()){
            this.todos.push({
                id : this.id++,
                description : ev.target.value,
                isComplete : false
            })
            ev.target.value = ""
        }
    }
    toggleTodoitem(todo){
        todo.isComplete = !todo.isComplete
    }
    deleteTodoitem(todo){
        const index = this.todos.findIndex((elem) => elem.id === todo.id);
        if (index >= 0){
            this.todos.splice(index,1);
        }
    }
    static components = {TodoItem};
}
