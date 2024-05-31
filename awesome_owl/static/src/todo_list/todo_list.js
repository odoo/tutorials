/** @odoo-module **/

import { Component, useState } from "@odoo/owl";
import { TodoItem } from "./todo_item";

export class TodoList extends Component {
    static template = "awesome_owl.TodoList";
    static components = {TodoItem};

    setup(){
        this.countIds = 0;
        this.todo = useState([]);
    }

    addTodo(ev){
        if (ev.keyCode === 13 && ev.target.value != ""){
            this.todo.push({id: this.countIds++, description: ev.target.value, isComplete: false});
            ev.target.value = "";
        }
    }

}
