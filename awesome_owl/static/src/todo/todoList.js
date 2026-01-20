/** @odoo-owl */
import { Component , useRef, useState, onMounted } from '@odoo/owl'
import { TodoItem } from './todoItem';

export class TodoList extends Component{
    static template = 'awesome_owl.todolist';
    static components = {TodoItem};
    setup(){
        this.todos = useState([]);
        this.inputRef = useRef('input_todo')
        onMounted(() => {
            this.inputRef.el.focus();
        });
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
        console.log(this.todos)
        if(!this.todos) return
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
