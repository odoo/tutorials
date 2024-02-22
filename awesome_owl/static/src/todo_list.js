/** @odoo-module **/

import { Component, useState, useRef, onMounted } from "@odoo/owl";

import { useAutoFocus } from "./utils";

import {TodoItem} from "./todo_item"

export class TodoList extends Component {

    static template = "awesome_owl.todo_list"
   
    setup() {
        this.todos = useState([]);
        this.state = useState({nextID: 0});
        useAutoFocus("refinput_todo");
    }

    
    static components = { TodoItem }

    addTodo(ev) {
        if(ev.keyCode == 13 && ev.target.value) {
            this.todos.push(
                {
                    id: this.state.nextID++,
                    description: ev.target.value,
                    isCompleted: false
                }
            )
        }
    }

    toggleItem(id, value) {
        const index = this.todos.findIndex((elem) => elem.id === id);
        if (index >= 0) {
            this.todos[index].isCompleted = value;
        }
    }

    remove(id) {
        const index = this.todos.findIndex((elem) => elem.id === id);
        if (index >= 0) {
            // remove the element at index from list
            this.todos.splice(index, 1);
        }
    }

}
