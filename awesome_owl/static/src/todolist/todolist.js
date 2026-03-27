import { useState, Component } from "@odoo/owl";
import { TodoItem } from "./todoitem";
import { useAutoFocus } from "../utils";

export class TodoList extends Component {
    static template = "awesome_owl.todolist";
    static components = { TodoItem };
    static props = []
    
    setup() {
        this.todos = useState([]);
        this.idCounter = 0
        useAutoFocus("todolist_input");
    }

    addTodo(ev) {
        if (ev.keyCode === 13 && ev.target.value) {
            this.todos.push({id: this.idCounter, description: ev.target.value, isCompleted: false})
            this.idCounter++
            ev.target.value = ''
        }
    }

    removeTodo(idToRemove) {
        const index = this.todos.findIndex(todo => todo.id === idToRemove);
        if (index !== -1) {
            this.todos.splice(index, 1);
        }
    }

}
