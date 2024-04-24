/** @odoo-module **/

import { Component, useState } from "@odoo/owl";
import { TodoItem } from "./todo_item";

export class TodoList extends Component {
    static template = "awesome_owl.todo_list";
    static components = { TodoItem };

    setup() {
        this.todos = useState([]);
        this.todoCounter = useState({value: 1});
    }

    addTodo(e){
        if (e.keyCode === 13 && e.target.value){
            this.todos.push({ 
                id: this.todoCounter.value,
                description: e.target.value,
                isCompleted: false
            });
            this.todoCounter.value++;
            e.target.value = '';
        }
    }
}
