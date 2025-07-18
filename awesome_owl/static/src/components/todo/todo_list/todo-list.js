/** @odoo-module **/

import { Component, useState} from "@odoo/owl";
import { TodoItem } from "../todo_item/todo_item";
import { useAutofocus } from "@awesome_owl/utils/utils";


export class TodoList extends Component {
    static template = "awesome_owl.todo_list";
    static components = {TodoItem};
    static props = {}; 


    setup() {
        this.todos = useState([]);
        this.ID = 1;
        this.todoInput = useAutofocus("todoInput"); 

    }

    addTodo(event){
        if(event.keyCode == 13){
            const inputVal = event.target.value.trim();

            if(inputVal.length === 0){
                return;
            }

            this.todos.push({
                id: this.ID++,
                description: inputVal,
                isCompleted: false,
            });
            
            event.target.value = "";
        } 
    }

    toggleState = (todoId) => {
        const todo = this.todos.find(t => t.id === todoId);
        if (todo) {
            todo.isCompleted = !todo.isCompleted;
        } else {
            console.error("Todo not found for id:", todoId);
        }
    };

    removeTodo = (todoId) => {
        const index = this.todos.findIndex(t => t.id === todoId);
        if (index >= 0) {
            this.todos.splice(index, 1);
        } else {
            console.error("Todo not found for id:", todoId);
        }
        
    };



}
