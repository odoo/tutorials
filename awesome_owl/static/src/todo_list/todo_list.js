/** @odoo-module **/

import { Component, useState, useRef, onMounted} from "@odoo/owl";
import { TodoItem } from "./todo_item/todo_item"
import { useAutoFocus } from "./../utils"


export class TodoList extends Component {
    static template = "awesome_owl.todo_list";
    static components = { TodoItem }

    setup() {
        this.todos = useState([]);
        useAutoFocus('todo_input');
        this.toggleTodoState = this.toggleTodoState.bind(this);
        this.removeTodoState = this.removeTodoState.bind(this);
    }

    addTodo(ev) {
        console.log("creating a Todo")
        if(ev.keyCode === 13 && ev.target.value){
            this.todos.push({ id: this.todos.length, description: ev.target.value, isCompleted: false });
        }
    }

    toggleTodoState(index) {
        const target = this.todos[index];
        target.isCompleted = !target.isCompleted
    }

    removeTodoState(index) {
        if (index !== -1) {
            this.todos.splice(index, 1);
        }
    }
}
