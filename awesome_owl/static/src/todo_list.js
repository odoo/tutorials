/** @odoo-module **/

import { Component, useState } from "@odoo/owl";
import { TodoItem } from "./todo_item";
import { useAutofocus } from "./utils";

export class TodoList extends Component {
    static template = "awesome_owl.todo_list"; 
    static components = { TodoItem };
    static props = [];

    setup(){
        this.todos = useState([
            { id: 1, description: "buy milk", isCompleted: true },
            { id: 2, description: "feed cat", isCompleted: false },
        ]);
        this.nextId = 3;
        this.inputRef= useAutofocus("newTodoInput");
    }

    addTodo(ev){
        if (ev.keyCode == 13){
            const text = this.inputRef.el.value.trim();
            if (!text) return;

            this.todos.push({
                id: this.nextId++,
                description: text,
                isCompleted: false,
            });
            this.inputRef.el.value = "";
        }
    }

    toggleState(id){
        //update isCompleted in the corresponding todo_item
        const todo = this.todos.find(t => t.id === id);
        if(todo){
            todo.isCompleted = !todo.isCompleted;
        } 
    }

    removeTodo(id){
        const index = this.todos.findIndex((elem) => elem.id === id);
        if (index >= 0) {
            // remove the element at index from list
            this.todos.splice(index, 1);
        }
    }
}
