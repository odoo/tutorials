import { Component, useState } from "@odoo/owl";
import { TodoItem } from "./todoitem";

export class TodoList extends Component {
    static template = "TodoList";
    static components = { TodoItem };

    setup(){
        this.todos = useState([]);
        this.nextId = 1;
    }

    addTodo(ev){
        if (ev.keyCode == 13 ){
            this.todos.push({
                id: this.nextId,
                description: ev.target.value,
                isCompleted: false
            });
            this.nextId++;
            ev.target.value = "";
        }
    }
}
