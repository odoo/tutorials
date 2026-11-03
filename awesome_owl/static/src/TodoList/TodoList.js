import { Component, useState } from "@odoo/owl";
import { TodoItem } from "../TodoItem/TodoItem";
import { useAutoFocus } from "../utils";

export class TodoList extends Component 
{
    static template = 'awesome_owl.TodoList';
    static components = { TodoItem };
    static props = {};
    setup()
    {
        this.todos = useState([]);
        this.ids = 0;
        useAutoFocus('todo_input');
    }
    addTodo(event)
    {
        if (event.type !== 'keyup' || event.keyCode !== 13 || event.target.value == "" )
            {
                return;
            }
        this.todos.push({id:this.ids++,description:event.target.value,isCompleted:false});
        event.target.value = "";
        
    }
    updateTodo(id)
    {
        let selectedTodo = this.todos.find(todo => todo.id == id);
        if(selectedTodo)
            {
                selectedTodo.isCompleted = !selectedTodo.isCompleted;
            }
        
    }
    deleteTodo(id)
    {
        const selectedTodo = this.todos.findIndex(todo => todo.id == id);
        if(selectedTodo >= 0)
            {
                this.todos.splice(selectedTodo, 1);
            }


    }

}