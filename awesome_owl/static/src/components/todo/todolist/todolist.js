import { Component, useState, useRef } from "@odoo/owl"
import { TodoItem } from "../todoitem/todoitem";
import { useAutofocus } from '../../../utils.js';


export class TodoList extends Component {
    static template = "awesome_owl.todolist"
    static components = { TodoItem }
    static props = {}

    setup() {
        super.setup();
        this.todos = useState([]);
        this.todoInputRef = useRef("todoInputRef");
        this.markTodo = this.markTodo.bind(this);

        useAutofocus("todoInputRef");

    }

    addTodo(ev) {
        if(ev.keyCode == 13) {
            let max_id = Math.max(...this.todos.map(todo => todo.id), 0);
            let new_description = this.todoInputRef.el.value;
            this.todos.push({ id: max_id + 1, description: new_description, isCompleted: false});
            this.todoInputRef.el.value = "";
        }
    }

    markTodo(todo_id) {
        this.todos.forEach((todo, index) => {
            if (todo.id == todo_id) {
                todo.isCompleted = !todo.isCompleted;
            }
        });
    }

    deleteTodo(todo_id) {
        this.todos.forEach((todo, index) => {
            if (todo.id == todo_id) {
                this.todos.splice(index,1)
            }
        });
    }
}
