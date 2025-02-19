/** @odoo-module **/

import { Component, useState, useRef } from '@odoo/owl';
import { TodoItem } from './todo_item';

export class TodoList extends Component{
    static template = "awesome_owl.todo_list";
    static components = { TodoItem }

    setup(){
        this.todos = useState([]);
        this.id = 1;
        this.inputRef = useRef("todoInput");
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

}
