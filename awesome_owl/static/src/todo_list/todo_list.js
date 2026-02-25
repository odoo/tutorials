import { Component, useState, useRef, onMounted } from "@odoo/owl";
import { TodoItem } from "../todo_item/todo_item";
import { useAutoFocus } from "../utils";

export class TodoList extends Component {
    static template = "awesome_owl.TodoList";
    static components = { TodoItem};

    setup() {
        super.setup();

        this.state = useState({
            todos: [
                { id: 1, description: "Buy milk", isCompleted: false },
                { id: 2, description: "Go to the gym", isCompleted: true },
                { id: 3, description: "Read a book", isCompleted: false },
            ],
            lastId: 3,
        });

        this.todoInputRef = useRef("todoInput");
        useAutoFocus(this.todoInputRef);
    }

    onKeyupTask(ev) {
        if (ev.key === "Enter") {
            if (!ev.target.value) {
                return;
            }
            
            this.#pushTodo(ev.target.value);

            ev.target.value = "";
        }
    }

    #pushTodo(description) {
        this.state.lastId += 1;

        const todo = {
            id: this.state.lastId,
            description: description,
            isCompleted: false,
        }

        this.state.todos.push(todo);
    }

    switchIsCompleted(id) {
        this.state.todos = this.state.todos.map(todo => todo.id === id ? {...todo, isCompleted: !todo.isCompleted} : todo);
    }

    deleteTodo(id) {
        this.state.todos = this.state.todos.filter(todo => todo.id !== id);
    }

    addTodo() {
        if (!this.todoInputRef.el.value) {
            return;
        }

        this.#pushTodo(this.todoInputRef.el.value);

        this.todoInputRef.el.value = "";    
    }        
}