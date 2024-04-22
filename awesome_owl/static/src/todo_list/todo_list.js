/** @odoo-module **/

import { Component, useState, useRef, useComponent, useEnv } from "@odoo/owl";
import { useAutoFocus } from "../utils";
import { TodoItem } from "./todo_item"

export class TodoList extends Component {
    static template = "awesome_owl.TodoList";
    static components = { TodoItem }

    setup() {
        this.todosCount = 0,
        this.state = useState({
            todos: [],
        })
        useAutoFocus("todoInputRef")
    }

    addTodo(event){
        if(event.keyCode === 13){
            if(event.target.value){
                this.state.todos.push({
                    id: ++this.todosCount,
                    description: event.target.value,
                    isCompleted: false
                })
                event.target.value = ""
            }
        }
    }
}
