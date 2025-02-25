import { Component, useState } from "@odoo/owl";
import { TodoItem } from "../todoitem/todoitem";
import { useAutoFocus } from "../utils"; 

export class TodoList extends Component {
    static template = "awesome_owl.TodoList";
    static components = {TodoItem};

    setup() {
        this.todos = useState([]);
        this.nextId = 0;
        useAutoFocus("addTask");
    }

    addTodo(ev) {
        if (ev.keyCode === 13 && ev.target.value) {
            this.todos.push({
                id: this.nextId++,
                description: ev.target.value,
                isCompleted: false
            });
            ev.target.value = ""
        }
    }

    toggleTodo(todo){  
        todo.isCompleted = !todo.isCompleted;
    }

    remTodo(todo) {
        const index = this.todos.findIndex((td) => td.id === todo.id);
        if (index >= 0) {
            this.todos.splice(index, 1);
        }
    }
}
