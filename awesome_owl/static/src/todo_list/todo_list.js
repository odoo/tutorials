import {Component, useState} from "@odoo/owl";
import { TodoItem } from "./todo_item";
import { useAutoFocus } from "../utils";

export class TodoList extends Component{
    static template = "awesome_owl.TodoList";
    static components = { TodoItem };
    static props = {};

    setup(){
        this.nextId = 0;
        this.todos = useState([]);
        useAutoFocus("input")
    }

    addTodo(ev){
        if (ev.keyCode !== 13 || ev.target.value === '') {
            return;
        }
        this.todos.push({
            id: this.nextId++,
            description: ev.target.value,
            isCompleted: false,
        });
        ev.target.value = '';
    }
}
