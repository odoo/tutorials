/** @odoo-module **/

import { Component, useState, useRef, onMounted } from "@odoo/owl";
import { TodoItem } from "./todoitem";


export class TodoList extends Component {
    static template = "awesome_owl.todolist";
    static components = {TodoItem};  

    setup(){
        this.myRef = useRef("todoInput")
        this.todos = useState([]);
        onMounted(() => {
            this.myRef.el.focus();
         });
    }
    

    addTodo(event){
        if(event.key === "Enter"){
            if(event.target.value){
                this.todos.push({
                    id: (this.todos.length) + 1,
                    description: event.target.value,
                    isCompleted: false,
                });
                event.target.value=""
            }
            else{
                return;
            }
        }
    }
    removeTodo = (todo) => {
        this.todos.splice(this.todos.indexOf(todo), 1);
    }
}
