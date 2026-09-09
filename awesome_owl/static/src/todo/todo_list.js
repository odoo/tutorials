import { Component, useState } from "@odoo/owl";
import { TodoItem } from "./todo_item";
import { useAutofocus } from "../utils";

export class TodoList extends Component {
    static template = "awesome_owl.TodoList";
    static components = { TodoItem };

    setup() {
        this.todos = useState([]);
        this.nextId = 1;
        useAutofocus("input");
    }

    addTodo(ev) {
        if (ev.key === "Enter") {
            const text = ev.target.value.trim();
            if (text) {
                this.todos.push({
                    id: this.nextId++,
                    description: text,
                    isCompleted: false,
                })
                ev.target.value = "";
            }
        }
    }

    toggleTodo(todoId) {
        const todo = this.todos.find((t) => t.id === todoId);
        if (todo) {
            todo.isCompleted = !todo.isCompleted;
        }
    }

    removeTodo(todoId){
        const index = this.todos.findIndex((t)=>t.id===todoId);
        if(index >=0){
            this.todos.splice(index,1);
        }
    }
}