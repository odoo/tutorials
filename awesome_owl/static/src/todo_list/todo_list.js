/** @odoo-module **/

import { Component, useState, useRef, onMounted } from "@odoo/owl";
import { TodoItem } from "./todo_item";

export class TodoList extends Component {
    static template = "awesome_owl.TodoList";
    static components = {TodoItem};

    setup(){
        this.countIds = 0;
        this.todo = useState([]);
        this.inputRef = useRef("inputTodo");
        onMounted(() => {
           this.inputRef.el.focus();
        });
    }

    addTodo(ev){
        if (ev.keyCode === 13 && ev.target.value != ""){
            this.todo.push({id: this.countIds++, description: ev.target.value, isComplete: false});
            ev.target.value = "";
        }
    }

    toggleTodo(Id){
        const record = this.todo.find((record) => record.id === Id);
        if (record){
            record.isComplete = !record.isComplete;
        }
    }

    removeTodo(Id){
        const idx = this.todo.findIndex((record) => record.id === Id);
        if (idx >= 0){
            this.todo.splice(idx,1);
        }
    }
}
