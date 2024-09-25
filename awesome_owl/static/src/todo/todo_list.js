/** @odoo-module **/

import { Component, useState, useRef } from "@odoo/owl";
import { TodoItem } from "./todo_item";

export class TodoList extends Component {
    static template = "awesome_owl.todo_list";
    static components = {TodoItem};

    setup (){
        this.todos = useState([]);
        this.todo_counter = 0
        this.inputRef = useRef('todo_input_field');
    }

    addTodo (event){
        if (event.key === "Enter"){

            var new_todo = document.getElementById("todo_input_field").value;
            if (new_todo !== ""){
                this.todo_counter++;
                this.todos.push({id: this.todo_counter, description:new_todo, isCompleted:false});
            }
        }
    }

    focusInputField (){
        this.inputRef.el.focus()
    }

    toggleCompletedTodo (id){
        const index = this.todos.findIndex((todo) => todo.id === id);
        if (index >= 0){
            this.todos[index].isCompleted = !this.todos[index].isCompleted
        }
    }

    removeTodo(id){
        const index = this.todos.findIndex((todo) => todo.id === id);
        if (index >= 0){
            this.todos.splice(index, 1);
        }
    }

}
