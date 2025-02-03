/** @odoo-module **/

import { Component, useState, useRef, onMounted } from "@odoo/owl";
import {TodoItem} from "./todo_item"
import {useAutoFocus} from '../utils'

export class TodoList extends Component {
    static template = "awesome_owl.todo_list"
    static components = {TodoItem}
    static id=0
    
    setup() {
        this.addNewTodoRef= useRef('addNewTodoRef')
        this.todos = useState([]);
        useAutoFocus(this.addNewTodoRef);
    }
     
    addTodo(ev) {
        if(ev.keyCode===13 && ev.target.value!=='') {
            TodoList.id++;
            this.todos.push({
                id: TodoList.id,
                description: ev.target.value,
                isCompleted: false
            })
            ev.target.value=""
        }
    }

    toggleState(todo_id) {
        for(let i=0;i<this.todos.length;i++) 
            if(this.todos[i].id=== todo_id) 
                this.todos[i].isCompleted = true
    }

    removeTodo(todo_id) {
        const index = this.todos.findIndex((item) => item.id === todo_id);
        if (index >= 0)
            this.todos.splice(index, 1);

    }
}
