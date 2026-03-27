import { Component, useState, useRef, onMounted } from "@odoo/owl";
import { TodoItem } from "./todo_item";
import { useAutofocus } from "../utils";

export class TodoList extends Component {
    static template = "awesome_owl.todo_list";
    static components = { TodoItem };

    static props = {
    }

    setup() {
        this.todos = useState([]);
        this.nextId = 0;
        this.showCompleted = useState({value: false})
        this.inputRef = useAutofocus("input");
        this.filtered = useState({value: "all"})
    }

    addTodo(ev) {
        if (ev.keyCode === 13) {   
            const value = ev.target.value;

            if (!value) {
                return; 
            }

            this.todos.push({
                id: this.nextId++,
                description: value,
                isCompleted: false,
            });

            ev.target.value = ""; 
        }
    }

    deleteTodo = (id) => {
        const index = this.todos.findIndex(todo => todo.id === id);

        if (index !== -1) {
            const todo = this.todos[index];

            this.todos.splice(index, 1);
        }
    }


    toggleTodo = (id) => {
        const todo = this.todos.find((todo) => todo.id === id);
        console.log(todo)
        if(todo) {
            todo.isCompleted = !todo.isCompleted;
        }
    }

    deleteCompletedTodos = () => {
        for (let i = this.todos.length - 1; i >= 0; i--) {
            if (this.todos[i].isCompleted) {
                this.todos.splice(i, 1);
            }
        }
    }

    filterMethod = (variable) => {
        // if(this.filtered.value == variable) return;
        if(variable == 'completed') this.showCompleted.value = true;
        this.filtered.value = variable;
    }
}