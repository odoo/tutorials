import { Component, useState } from "@odoo/owl";
import { Todoitem } from "./todoitem";

export class Todolist extends Component {

    static template = "awesome_owl.Todolist";
    static components = { Todoitem };

    setup() {
        this.state = useState({
            todos: [],
            newTodo: "",
            nextId: 1
        });
        this.removeTodo = this.removeTodo.bind(this);
    }

    addTodo(ev) {
        if (ev.keyCode === 13 && this.state.newTodo.trim()) {
            const newTodo = {
                id: this.state.nextId++,
                description: this.state.newTodo,
                isCompleted: false
            };
            this.state.todos = [...this.state.todos, newTodo];
            this.state.newTodo = "";
        }
    }

    toggleState(todo) {
        todo.isCompleted = !todo.isCompleted
    }

    removeTodo(todo) {   
        const todo1 = this.state.todos.find((t)=>(t.id===todo.id));
        this.state.todos.splice(todo1,1);
    }
}
