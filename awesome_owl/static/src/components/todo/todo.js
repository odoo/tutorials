import { Component, useState } from "@odoo/owl"

import { useInputFocus } from "../../utils/utils"

export class TodoItem extends Component {
    static template = "awesome_owl.todo.item" 
    static props = {
        todo: {
            type: Object,
            shape: {
                id: Number,
                description: String,
                isCompleted: Boolean
            }
        },
        removeTodo: Function
    }
}

export class TodoList extends Component {
    static components = { TodoItem }
    static template = "awesome_owl.todo.list"

    setup() {
        this.todos = useState([]);
        this.description_input = useState({
            val: ""
        });
        useInputFocus("todo_in");
    }

    addTodo(ev) {
        if(ev.keyCode == 13){
            this.todos.push({
                id: this.todos.length + 1,
                description: this.description_input.val,
                isCompleted: false
            })
            this.description_input.val = "";
        }
    }

    removeTodo(id) {
        // the id is 1-based
        this.todos.splice(id-1, 1)
    }
}
