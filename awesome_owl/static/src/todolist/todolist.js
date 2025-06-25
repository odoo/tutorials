import { Component, useState, useRef, onMounted } from "@odoo/owl";
import { TodoItem } from "./todoitem";

export class TodoList extends Component {
    static template = "my_module.TodoList";
    
    static components = {TodoItem}

    setup() {
        this.todos = useState([]);
        this.inputRef = useRef('focus-input');
        onMounted(() => {
            this.inputRef.el.focus()
        });
    }

    toggleTodo(id) {
        const todo = this.todos.find(todo => todo.id === id);
        if (todo){
            todo.isCompleted = !todo.isCompleted
        }
    }

    removeTodo(id) {
        const index = this.todos.findIndex(todo => todo.id === id);
        if (index !== -1) {
            this.todos.splice(index, 1);
        }
    }

    addTodo(ev){
        if (ev.keyCode === 13){
            this.todos.push({id: this.todos.length + 1, description: ev.target.value.trim(), isCompleted: false})
            ev.target.value = "" //reinit
        }

    }
}
