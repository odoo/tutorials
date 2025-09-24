import { Component, useState, onMounted, } from "@odoo/owl";
import { TodoItem } from "./todo_item";
import { useAutofocus } from "../utils";


export class TodoList extends Component {
    static template = "awesome_owl.todo_list";
    static components = { TodoItem };

    static props = {};

    setup() {
        this.todos = useState([
            { id: 1, description: "buy milk", isCompleted: true },
            { id: 2, description: "buy cheese", isCompleted: false },
            { id: 3, description: "buy bread", isCompleted: false }]);
        useAutofocus(this, "todoInput");
    }

    addTodo(event) {
        if(event.key === "Enter" && event.target.value.trim() !== ""){
            const newId = this.todos.length ? Math.max(...this.todos.map(t => t.id)) +1 : 1;
            this.todos.push({
                id: newId,
                description: event.target.value.trim(),
                isCompleted: false
            });
            event.target.value = "";
        }
    }

    removeTodo(elemId){
        const index = this.todos.findIndex((elem) => elem.id === elemId);
        if(index >= 0){
            this.todos.splice(index, 1);
        }
    }

    toggleTodoState(id, state){
        const todo = this.todos.find(t => t.id === id);
        if(todo){
            todo.isCompleted = state;
        }
    }
}
