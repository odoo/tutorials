/** @odoo-module **/

import { Component,useState } from "@odoo/owl";
import { TodoItem } from "./todoItem";

export class TodoList extends Component{

    static template = "awesome_owl.todoList";
    static components = {TodoItem};
    static props = {}
    setup()
    {
        this.id = useState({value : 0});
        this.todos = useState([]);
        this.toggle = this.toggle.bind(this);
        this.deleteTodo = this.deleteTodo.bind(this);
    }

    addTodo(event)
    {
        if(event.keyCode == 13 && (event.target.value).trim() != "")
        {
            this.todos.push({id : this.id.value++, description: event.target.value, isCompleted: false});
            event.target.value = "";
        }
    }

    toggle(itemId){
        let todoItem = this.todos.find(todo => todo.id == itemId);
        todoItem.isCompleted = !todoItem.isCompleted;
    }

    deleteTodo(todoId)
    {
        let todoIndex = this.todos.findIndex(todo => todo.id == todoId)
        this.todos.splice(todoIndex,1)
    }
}
