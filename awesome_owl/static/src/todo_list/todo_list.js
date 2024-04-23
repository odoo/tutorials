/** @odoo-module **/

import { Component, useState, useRef, useComponent, useEnv } from "@odoo/owl";
import { TodoItem } from "./todo_item"
import { useAutoFocus } from "../utils";
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

    toggleTodoItemState(todoItemId){
        const todoItem = this.state.todos.find((todoItem) => todoItem.id === todoItemId)
        todoItem.isCompleted = !todoItem.isCompleted 
    }

    removeTodoItem(todoItemId){
        const todoItemIndexInTodos = this.state.todos.findIndex((todoItem) => todoItem.id === todoItemId)
        if(todoItemIndexInTodos >= 0){
            this.state.todos.splice(todoItemIndexInTodos, 1)
        }
    }
}
