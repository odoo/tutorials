import {Component, useState} from "@odoo/owl"
import {TodoItem} from "./todo_item";
import {useAutofocus} from "../utils";


export class TodoList extends Component {
    static template = "awesome_owl.todo.list";

    static components = {TodoItem};

    static idGen = 0;

    static get id() {
        return this.idGen++;
    }

    setup() {
        this.todos = useState([]);
        useAutofocus('todo_input');
        this.toggleTodo = this.toggleTodo.bind(this);
        this.deleteTodo = this.deleteTodo.bind(this);
    }

    addTodo(event) {
        if (event.keyCode === 13 && event.target.value) {
            this.todos.push(
                {
                    id: this.constructor.id,
                    description: event.target.value,
                    isCompleted: false
                }
            );
            event.target.value = '';
        }
    }

    toggleTodo(id) {
        const idx = this.todos.findIndex((elem) => elem.id === id);
        if(idx !== -1) {
            this.todos[idx].isCompleted = !this.todos[idx].isCompleted;
        }
    }

    deleteTodo(id) {
        const idx = this.todos.findIndex((elem) => elem.id === id);
        if(idx !== -1) {
            this.todos.splice(idx, 1);
        }
    }
}
