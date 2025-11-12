/** @odoo-module **/

import { Component, useState } from "@odoo/owl";
import { TodoItem } from "./todo_item"

export class TodoList extends Component {
    static template = "awesome_owl.todolist";
    static components = { TodoItem }
    static props = {}
    setup(){
        this.todos = useState([
            { id: 0, description: "Do something", isCompleted: true },
            { id: 1, description: "Do something else", isCompleted: false },
            { id: 2, description: "Do stuff", isCompleted: false },
            { id: 3, description: "Do more stuff", isCompleted: false }
        ]);
    }
    todoListAddItem(input_value) {
        if (input_value.keyCode === 13 && input_value.target.value){
            this.todos.push({id: (this.todos.length) ? this.todos.at(-1).id + 1 : 0, description: input_value.target.value, isCompleted: false});
            input_value.target.value = "";
        } 
    }
    todoListToggleItem(todoId) {
        this.todos.forEach((todo) => {
            if (todo.id === todoId) {
                todo.isCompleted = !todo.isCompleted;
            }
        })
    }
    todoListRemoveItem(todoId) {
        this.todos.forEach((todo) => {
            if (todo.id === todoId) {
                this.todos.splice(todoId, 1);
                for (let i = 0; i < this.todos.length; i++) {
                    this.todos.at(i).id = i
                }
            }
        })
    }
}
