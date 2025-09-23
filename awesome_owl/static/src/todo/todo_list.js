import { Component, useState } from "@odoo/owl";

import { TodoItem } from "./todo_item"; 

export class TodoList extends Component {
    static template = "awesome_owl.todo_list";
    static components = { TodoItem }; 

    setup() {
        this.todos = useState([]);
        this.state = useState({ counter_id : 0});
    }

    addTodo(ev) {
        if (ev.keyCode === 13 && ev.target.value){
            const newTodo = {
                id : this.state.counter_id,
                description : ev.target.value,
                isCompleted : false,
            }
            this.state.counter_id ++;
            this.todos.push(newTodo);
            ev.target.value = "";
        };
        
    }
}

