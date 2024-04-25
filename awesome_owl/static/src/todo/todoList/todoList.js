/** @odoo-module **/

import { Component, useState, useRef, onMounted } from "@odoo/owl";
import { TodoItem } from "../todoItem/todoItem";
import { useAutofocus } from "../utils";

export class TodoList extends Component {
    static template = "awesome_owl.TodoList";

    static components = { TodoItem };

    setup(){
        this.todos = useState([]);
        this.id = 0;
        useAutofocus("input");
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

    toggleTodo(todoId){
        const todo = this.todos.find((todo) => todo.id === todoId);
        if (todo){
            todo.flag = !todo.flag;
        }
    }
}
