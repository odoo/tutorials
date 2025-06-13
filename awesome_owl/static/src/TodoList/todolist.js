import { Component, useRef, useState, onMounted } from "@odoo/owl"
import { TodoItem } from "./todoitem"
import { useAutofocus } from "./utils"

export class TodoList extends Component{
    static template = "awesome_owl.todolist"
    static components = { TodoItem }

    // inputref = useRef('input');

    setup(){
        this.todos = useState([]);
        this.counter = 1;
        
        useAutofocus("input")
    }

    addTodo(ev){
        if(ev.keyCode === 13 && ev.target.value !== ""){
            this.todos.push({id:this.counter++, description: ev.target.value, isComplete: false});
            ev.target.value = '';
        }
    }

    toggleState(id){
        const index = this.todos.findIndex((elem) => elem.id === id);
        this.todos[index].isComplete = !(this.todos[index].isComplete);
    }

    removeTodo(id){
        const index = this.todos.findIndex((elem) => elem.id === id); 
        if (index >= 0) {
            // remove the element at index from list
            this.todos.splice(index, 1);
        }
    }

}
