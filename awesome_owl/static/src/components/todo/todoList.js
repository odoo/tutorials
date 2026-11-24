import {Component, useState, useRef, onMounted} from '@odoo/owl';
import { TodoItem } from './todoItem';

export class TodoList extends Component{
    static template = 'awesome_owl.todoList'
    static components = {TodoItem}

    setup(){
        this.todos = useState([]);
        this.inputRef = useRef('input')
        this.nextId = 0
        onMounted(()=>{
            this.inputRef.el.focus()
        })
    }

    addTodo(ev){
        if(ev.keyCode==13){
            const description = ev.target.value.trim()

            if(!description){
                return;
            }
            this.nextId+=1

            this.todos.push({
                id:this.nextId,
                description:description,
                isCompleted:false
            })

            ev.target.value="";
        }
    }

    markTodo(todoId){        
        this.todos[todoId-1].isCompleted = !this.todos[todoId-1].isCompleted
    }

    deleteTodos(todoId){
        console.log("Todo LIst",todoId);
        const index = this.todos.findIndex(el=>el.id===todoId)
        this.todos.splice(index,1)
    }

}