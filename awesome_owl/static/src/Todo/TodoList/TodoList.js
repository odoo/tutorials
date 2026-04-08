import { Component, useState } from "@odoo/owl";
import { TodoItem } from "../TodoItem/TodoItem";
import { useAutofocus } from "../../utils"

export class TodoList extends Component {
    static template = "awesome_owl.TodoList";

    setup() {
        this.nextId = 1;
        this.todos = useState([]);
        useAutofocus("input")
    }

    toggleState(todoId) {
        const todo = this.todos.find((todo) => todo.id === todoId)

        if (todo) {
            todo.isCompleted = !todo.isCompleted;
        }
    }

    deleteTodo(todoId) {
        const index = this.todos.findIndex((todo) => todo.id === todoId);
        if (index >= 0) {
            // remove the element at index from list
            this.todos.splice(index, 1);
            console.log(index);
            if(this.nextId > 1){
                this.nextId = 1
                this.todos.forEach(todo => {
                    todo.id = this.nextId++
            });}
        }
    }

    addTodo(ev) {
        if (ev.key === "Enter" && ev.target.value != "") {
            this.todos.push({
                id: this.nextId++,
                description: ev.target.value,
                isCompleted: false
            })
            ev.target.value = "";
        };
    }

    static components = { TodoItem }
}
