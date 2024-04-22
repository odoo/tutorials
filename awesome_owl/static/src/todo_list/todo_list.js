/** @odoo-module **/

import { Component, useState } from "@odoo/owl";
import { TodoItem } from "./todo_item"

export class TodoList extends Component {
    static template = "awesome_owl.TodoList";
    static components = { TodoItem }

    setup() {
        this.todosCount = 0,
        this.state = useState({
            todos: [],
        })
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
