/** @odoo-module **/

import { Component, useState} from "@odoo/owl";
import { TodoItem } from "./todoitem";
import { useAutofocus } from "../utils";

export class TodoList extends Component {
    
    static template = "awesome_owl.todolist";
    static components = { TodoItem }

    setup(){
        this.state = useState({
            todo: [],
            uid: 1
        });
        useAutofocus();
        this.toggleState = this.toggleState.bind(this)
        this.removeTodo = this.removeTodo.bind(this)
    }

    // Adding todo
    addTodo(e){
        const input = e.target;
        const value = input.value.trim();
        
        // Check if Enter was pressed and value is not empty
        if(e.keyCode == 13 && value !== ""){
            this.state.todo.push({
                id: this.state.uid,
                description: value,
                isCompleted: false
            });
            this.state.uid++;
            input.value = "";
        }
    }

    // Mark todo as done
    toggleState(todoId, isCompleted){
        const todo = this.state.todo.find(ele => ele.id === todoId);
        if(todo){
            todo.isCompleted = isCompleted;
        }
    }

    //delete todo from list
    removeTodo(todoId){
        this.state.todo = this.state.todo.filter(ele => ele.id !== todoId);   
    }
}
