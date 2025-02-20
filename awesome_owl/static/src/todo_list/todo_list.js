import { Component, useState } from "@odoo/owl";
import { TodoItem } from "./todo_item";

export class TodoList extends Component {
    static template = "awesome_owl.TodoList";

    setup(){
        this.nextId = 0;
        this.todos = useState([]);
    }

    addTodo(ev){
        if(ev.keyCode === 13 && ev.target.value.trim()){
            this.todos.push({
                id: this.nextId+=1,
                description: ev.target.value,
                isCompleted: false
            });
            ev.target.value = "";
        }
    }

    static components = { TodoItem };
}