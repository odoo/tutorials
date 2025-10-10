/** @odoo-owl */

import { Component , useRef, useState, onMounted } from '@odoo/owl'
import { TodoItem } from './todo_item';
import { useAutofocus } from '../utils';

export class TodoList extends Component{
    static template = 'awesome_owl.todolist';

    setup(){
        this.todos = useState([
            { id: 1, description: "Buy milk", isCompleted: false },
            { id: 2, description: "Complete project", isCompleted: true },
            { id: 3, description: "Call mom", isCompleted: false },
        ]);
        this.myRef = useRef('input_todo')
        // onMounted(() => {
        //     this.myRef.el.focus();
        // });
        useAutofocus(this.myRef)
    }

    addTodo(ev){
        if(ev.keyCode === 13){
            const description = ev.target.value.trim()
            if(description){
                this.todos.push({
                    id: this.todos.length + 1,
                    description: description,
                    isCompleted: false,
                })
                ev.target.value = ""
            }
        }
    }

    toggleState(todoId){
        const todo = this.todos.find((t) => t.id === todoId);
        if(todo){
            todo.isCompleted = !todo.isCompleted;
        }
    }

    removeTodo(todoId){
        const index = this.todos.findIndex((t) => t.id === todoId);
        if(index !== -1){
            this.todos.splice(index, 1)
        }
    }

    static components = { TodoItem };
}
