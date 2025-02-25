import { Component, useState } from "@odoo/owl";
import { TodoItem } from "./todo_item";
import { useAutoFocus } from "../utils";

export class TodoList extends Component {

    static template = "awesome_owl.TodoList" 

    static components = { TodoItem };

    setup(){
        
        this.nextId = 0;
        this.todos = useState([]);
        useAutoFocus("input")

    }
    
    addTodo(ev){
        if(ev.keyCode==13 && ev.target.value != ""){
            this.todos.push({
                id:this.nextId++,
                description:ev.target.value,
                isCompleted:false
            }); 
            ev.target.value="";
        }
    } 

    togleTodo(todoId){
           const todo = this.todos.find((todo) => todo.id === todoId); 

           if(todo){
              todo.isCompleted = !todo.isCompleted;
           }
    }

    removeTodo(todoId){
        const todoIndex = this.todos.findIndex((todo)=> todo.id === todoId);

        if (todoIndex>=0){
            this.todos.splice(todoIndex,1);
        }
    }
} 
