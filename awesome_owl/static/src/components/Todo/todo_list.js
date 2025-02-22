/** @odoo-module **/

import { Component, useState, useRef } from '@odoo/owl';
import { TodoItem } from './todo_item';
import { useAutofocus } from '../../utils/hooks';


export class TodoList extends Component{
    static template = "awesome_owl.todo_list";
    static components = { TodoItem }

    setup(){
        this.todos = useState([]);
        this.id = 1;
        this.inputRef = useRef("todoInput");
        useAutofocus(this.inputRef);
    }

    addTodo(ev){
        if(ev.keyCode === 13){
            const description = this.inputRef.el.value.trim();
            if(description){
                this.todos.push({
                    id: this.id++,
                    description,
                    isCompleted: false,
                });
                this.inputRef.el.value="";
            }
        }
    }

    toggleState(id){
        const todo = this.todos.find(t => t.id === id);
        if(todo){
            todo.isCompleted = !todo.isCompleted;
        }
    }

    deleteTodo(id){
        const indx = this.todos.findIndex(t => t.id === id);
        if(indx >= 0){
            this.todos.splice(indx, 1);
        }
    }

}
