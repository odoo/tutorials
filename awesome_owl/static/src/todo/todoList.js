import { Component, useState, useRef, onMounted } from '@odoo/owl';
import { TodoItem } from './todoItem';

class TodoList extends Component {
    setup() {
        this.todos = useState([]);
        this.inputRef = useRef("input");
        this.nextId = 1;

        onMounted(() => {
            this.inputRef.el.focus();
        });
    }

    addTodo(ev) {
        if (ev.keyCode === 13 && ev.target.value.trim()) {
            this.todos.push({
                id: this.nextId++,
                description: ev.target.value.trim(),
                isCompleted: false,
            });
            ev.target.value = "";
        }
    }

    toggleTodo(id) {
        const todo = this.todos.find(t => t.id === id);
        if (todo) {
            todo.isCompleted = !todo.isCompleted;
        }
    }

    removeTodo(id) {
        const index = this.todos.findIndex(t => t.id === id);
        if (index >= 0) {
            this.todos.splice(index, 1);
        }
    }

    static components = { TodoItem };
}

