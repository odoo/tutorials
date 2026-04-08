import { Component, useState } from "@odoo/owl";
import { TodoItem } from "./todo_item";
import { useAutofocus } from "../utils";

export class TodoList extends Component {
    static template = "awesome_owl.TodoList";
    static components = { TodoItem };

    setup() {
        this.todos = useState([]);
        this.uniqueId = 1;
        useAutofocus("text_todo_input");
    }

    addTodo(ev){
        if(ev.key === "Enter" && ev.target.value!=""){
           this.todos.push({
                id: this.uniqueId++,
                description: ev.target.value,
                isCompleted: false
            });
            ev.target.value = "";
        }
    }

    toggleTodo(todoId) {
        const newtodo = this.todos.find((todo) => todo.id === todoId);
        if (newtodo) {
            newtodo.isCompleted = !newtodo.isCompleted;
        }
    }

    removeTodo(todoId) {
        const todoIndex = this.todos.findIndex((todo) => todo.id === todoId);
        if (todoIndex >= 0) {
            this.todos.splice(todoIndex, 1);
        }
    }
}
