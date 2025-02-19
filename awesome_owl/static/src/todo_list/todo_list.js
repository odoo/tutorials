import {Component, useState, useRef, onMounted} from "@odoo/owl"
import { TodoItem} from "../todo_item/todo_item"
import {useAutoFocus} from "../utils"

export class TodoList extends Component{
    static template = "awesome_owl.TodoList"

    static components = {TodoItem}

    setup(){
        this.todos = useState([]);
        this.current_id = 1;
        useAutoFocus("input")

    }


    addTodo(ev){
        let task = ev.target.value.trim()
        if(ev.keyCode === 13 && task != ""){
            this.todos.push({
                id : this.current_id++,
                task: task,
                isCompleted: false
            })
            ev.target.value = "";
        }
    }
}
