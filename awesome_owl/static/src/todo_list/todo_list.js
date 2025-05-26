import { Component, useState } from "@odoo/owl";
import { Todo_item } from "./todo_item";

export class Todo_list extends Component {
    static template = "awesome_owl.Todo_list";
    static components = {Todo_item};
    static props = {};

    setup() {
        this.todos = useState([{ id: 1, description: "buy milk", isCompleted: true }]);
        this.nb_todo = 2;
    }

    addTodo(ev){
        if(ev.keyCode !== 13 || ev.target.value === "")
            return;
        this.todos.push({
            id: this.nb_todo++,
            description: ev.target.value,
            isCompleted: false,
        });
        console.log(this.todos);
        ev.target.value = "";
    }

    toggleTodo(todoId) {
        const todo = this.todos.find((todo) => todo.id === todoId);
        if (todo) {
            todo.isCompleted = !todo.isCompleted;
        }
    }

    removeTodo(todoId) {
        const todoIndex = this.todos.findIndex((todo) => todo.id === todoId);
        if (todoIndex >= 0) {
            this.todos.splice(todoIndex, 1);
        }
        this.todos.map((todo) =>{
            if(todo.id > todoId)
                todo.id --;
        })
        this.nb_todo --;
    }
}