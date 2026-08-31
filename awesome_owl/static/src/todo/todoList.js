import { Component, useState } from "@odoo/owl";
import { TodoItem } from "./todoItem";
import { useAutoFocus } from "../utils";

export class TodoList extends Component {
    static template = "awesome_owl.todoList";
    static components = { TodoItem };
    
    setup() {
        this.state = useState({todos: []});
        this.idCounter = 1;
        this.addTodoRef = useAutoFocus();
    }

    onAddTodo(ev) {
        if (ev.key == "Enter" && ev.target.value.trim() !== "") {
            const newTodo = {
                id: this.idCounter++,
                description: ev.target.value,
                isCompleted: false,
            };

            this.state.todos.push(newTodo);
            ev.target.value = "";
        } 
    }

    toggleState(todoId) {
        const todo = this.state.todos?.find((t) => t.id === todoId);
        if (todo) todo.isCompleted = !todo.isCompleted;
    }

    removeTodo(todoId) {
        this.state.todos = this.state.todos?.filter((t) => t.id !== todoId);
    }  
}
