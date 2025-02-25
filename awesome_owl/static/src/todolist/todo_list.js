import { Component, useState } from '@odoo/owl';
import { TodoItem } from './todo_item';

export class TodoList extends Component {
    static template = 'awesome_owl.TodoList';
    static components = { TodoItem };
    static props = {
        todos: {
            type: Array,
            optional: true,
        },
    };

    setup() {
        this.todos = useState([]);
        this.addTask = this.addTask.bind(this);
        this.nextTodoId = this.todos.length + 1;
    }

    addTask(ev) {
        ev.preventDefault();
        if (ev.key !== 'Enter') {
            return;
        }
        const input = ev.target;
        const description = input.value.trim();
        if (!description) {
            return;
        }
        this.todos.push({
            id: this.nextTodoId++,
            description,
            isCompleted: false,
        });
        input.value = '';
    }
}
