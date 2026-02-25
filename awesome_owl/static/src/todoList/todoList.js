import { Component, useState } from "@odoo/owl";
import { TodoItem } from "./todoItem/todoItem";

export class TodoList extends Component {
    static template = "awesome_owl.TodoList";

    setup() {
        this.todos = useState([]);
        this.id = 0;
    }

    addTodo(event){
        if (event.keyCode == 13){
            console.log(event)
            this.todos.push({id: this.id++, description: event.target.value, isCompleted:false})
        }
    }

    static components = { TodoItem };
}