/** @odoo-module **/

import { Component, onMounted, useRef, useState } from "@odoo/owl";
import { TodoItem } from "./todo_item";

export class TodoList extends Component {
    static template = "awesome_owl.todo_list";

    static components = { TodoItem };

    setup(){
        this.todos = useState([]);
        this.count = 1;
        this.inputRef = useRef('input_field');
        onMounted(() => {
            this.inputRef.el.focus();
        });
    }

    addTodo(ev){
        if(ev.key === "Enter" && ev.target.value)
        {
            this.todos.push({id: this.count++, description: ev.target.value, isCompleted: false});
            ev.target.value = "";
        }
    }

    removeTodo(todo_id) {
        const index = this.todos.findIndex((elem) => elem.id === todo_id);
        if(index >= 0) {
            this.todos.splice(index, 1);
        }
    }
}
