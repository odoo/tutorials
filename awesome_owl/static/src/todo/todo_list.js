import { Component, useState, useRef, onMounted } from "@odoo/owl";
import { TodoItem } from "./todo_item";

export class TodoList extends Component {
    static template = "awesome_owl.todo_list";
    static components = { TodoItem };

    setup() {
        this.todos = useState([]);
        this.nextId = 0;

        this.inputRef = useRef("todoInput");


        this.toggleTodo = (id) => {
            const todo = this.todos.find(t => t.id === id);
            todo.isCompleted = !todo.isCompleted;
        };

        this.removeTodo = (id) => {
            const index = this.todos.findIndex(t => t.id === id);
            if (index >= 0) {
                this.todos.splice(index, 1);
            }
        };
        
        onMounted(() => {
            this.inputRef.el.focus();
        });
    }

    addTodo(ev) {
        if (ev.keyCode !== 13) {
            return;
        }

        const value = ev.target.value.trim();
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
