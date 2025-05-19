import { Component, useState } from "@odoo/owl";
import { TodoItem } from "./todoitem";
import { UseAutofocus } from "../utils";

export class TodoList extends Component {
    static template = "TodoList";
    static components = { TodoItem };
    static props = [];

    setup(){
        this.todos = useState([]);
        this.nextId = 1;
        UseAutofocus("todo_input");
    }

    addTodo(ev){
        if (ev.keyCode == 13 && ev.target.value != ""){
            this.todos.push({
                id: this.nextId,
                description: ev.target.value,
                isCompleted: false
            });
            this.nextId++;
            ev.target.value = "";
        }
    }

    removeTodo(todoId){
        const todoIdInArray = this.todos.findIndex((todo) => todo.id == todoId);
        if (todoIdInArray >= 0) {
            this.todos.splice(todoIdInArray, 1);
        }
    }
}
