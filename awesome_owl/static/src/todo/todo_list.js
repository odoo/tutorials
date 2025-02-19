import { Component, onMounted, useRef, useState} from "@odoo/owl";
import { TodoItem } from "./todo_item";
import { useAutofocus } from "../utils";

export class TodoList extends Component{
    static template = "awesome_owl.TodoList";
    static components = { TodoItem };

    setup(){
        this.todos = useState([]);
        this.todoCount = 1;
        useAutofocus("input");
    };
    addTodo(ev){
        if(ev.keyCode === 13 && ev.target.value.trim() !== ""){
            this.todos.push({ id: this.todoCount++, description: ev.target.value.trim(), isCompleted: false });
            ev.target.value = "";
        }
    }
}
