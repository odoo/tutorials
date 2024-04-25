/** @odoo-module **/

import { Component, useState, useRef, onMounted } from "@odoo/owl";
import { TodoItem } from "../todoItem/todoItem";


export class TodoList extends Component {
    static template = "awesome_owl.TodoList";

    static components = { TodoItem };

    setup(){
        this.todos = useState([]);
        this.id = 0;
        this.myRef = useRef('input');
        onMounted(() => {
            this.myRef.el;
        })
    }

    addTodo(ev){
        if(ev.keyCode === 13 && ev.target.value != "")
        {
            this.todos.push({
                id: this.id++,
                description: ev.target.value,
                flag: false
            });
            ev.target.value = "";
        }
    }
}
