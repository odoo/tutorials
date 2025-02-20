import {Component, useState} from "@odoo/owl";
import {TodoItem} from "./todoItem"
import {useAutofocus} from "../utils"
export class TodoList extends Component{
    static template= "awesome_owl.todoList"
    static components= {TodoItem}
    setup(){
        this.todos= useState([{id:1, description:"write tutorial",isCompleted:true }, {id:2, description:"buy milk", isCompleted:false}])
        this.inputRef = useAutofocus('inputRef');
    }
    addTodo(ev){
        console.log(ev);
        console.log(ev.target.value);
        if(ev.keyCode===13 && ev.target.value!=""){
            let newid= this.todos.length+1
            this.todos.push({id:newid, description:ev.target.value, isCompleted:false})
            ev.target.value=""
        }
    }
    toggleTodoState(id){
        let todo= this.todos.find((item)=> item.id==id)
        if(todo){
            todo.isCompleted= !todo.isCompleted;
        }
    }
    removeTodo(id){
        let index= this.todos.findIndex((elem)=> elem.id==id);
        if(index>=0){
            this.todos.splice(index, 1)
        }
    }
}
