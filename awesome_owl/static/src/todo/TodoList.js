import {Component, useState, useRef , onMounted} from "@odoo/owl";
import {TodoItem} from "./TodoItem";

export class TodoList extends Component{
    static template= "awesome_owl.todo_list"
    static components = { TodoItem };

    setup(){
        this.todos=useState([]);
        this.toggleState=this.toggleState.bind(this);
        this.removeTodo=this.removeTodo.bind(this)
        this.todoId = 1;
        this.myRef=useRef('input_bar')
        onMounted(() => {
            if(this.myRef.el){
                this.myRef.el.focus()
            }
         });
    }

    addTodo(ev) {
        if (ev.keyCode === 13) {
            const input = ev.target;
            const description = input.value.trim();            
            if (description) {
                this.todos.push({
                    id: this.todoId++,
                    description: description,
                    isCompleted: false,
                });

                input.value = "";
            }
        }
    }
    toggleState(todoId) {
        const todo = this.todos.find(todo => todo.id === todoId);
        if (todo) {
            todo.isCompleted = !todo.isCompleted;
        }
    }
    removeTodo(todoId){
        const todo=this.todos.find(todo => todo.id === todoId); 
        this.todos.splice(todo, 1);
    }
}
