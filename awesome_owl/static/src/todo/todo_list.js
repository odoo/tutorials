import { Component, useState, useRef, onMounted } from "@odoo/owl";
import { TodoItem } from "./todo_item";

export class TodoList extends Component {
    static template="awesome_owl.todolist";

    static components = {TodoItem};

    setup() {
    this.todos = useState([]);  
    this.nextId = 0;

    this.inputRef = useRef("input");
    onMounted(() => {
        this.inputRef.el.focus();
            }     
        )
    }

    addTodo(ev) {
        if (ev.keyCode === 13) {
            const text = ev.target.value;

            if (!text) {
                return;
            }

            this.todos.push({
                id: this.nextId++,
                description: text,
                isCompleted: false
            });
            ev.target.value = "";
        }
    }

    toggleState(id) {
        const todo = this.todos.find(t => t.id === id);

        if (todo) {
            todo.isCompleted = !todo.isCompleted;
        }
    }

    removeTodo(id) {
        const index = this.todos.findIndex(t => t.id === id)

        if(index >= 0) {
            this.todos.splice(index, 1);
        }
    }
}
