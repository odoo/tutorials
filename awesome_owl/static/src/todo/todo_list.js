/** @odoo-module**/

import { onMounted, useRef, useState, Component } from "@odoo/owl";
import { TodoItem } from "./todo_item";
import { useAutoFocus } from "../utils";

export class TodoList extends Component {
    static template = "awesome_owl.todo_list";

    static components = { TodoItem };

    setup() {
        this.todos = useState([
            { id: 3, description: "buy milk", isCompleted: false },
            { id: 4, description: "testt", isCompleted: true },
        ]);
        this.state = useState({newTodo: ""});
        useAutoFocus("new_todo");
    }

    addTodo(ev) {
        if(ev.keyCode === 13 && this.state.newTodo){
            this.todos.push({
                id: (this.todos.length > 0 ? ((Math.max(...this.todos.map(t => t.id))) + 1) : 0),
                description: this.state.newTodo,
                isCompleted: false
            });
            this.state.newTodo = "";
        }
    }

    toggleState(id){
        this.todos[this.todos.findIndex(todo => todo.id === id)].isCompleted ^= true;
    }

    removeTodo(id){
        this.todos.splice(this.todos.findIndex(todo => todo.id === id), 1);
    }

}
