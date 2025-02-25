import { Component, useState } from '@odoo/owl';
import { TodoItem } from './todo_item';
import { useAutoFocus } from '../utils';

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
        useAutoFocus('add_task_input');
        this.toggleTodo = this.toggleTodo.bind(this);
        this.removeTodo = this.removeTodo.bind(this);
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

    toggleTodo(todoId) {
        const toBeToggled = this.todos.find(todo => todo.id === todoId);
        toBeToggled.isCompleted = !toBeToggled.isCompleted;
    }

    removeTodo(todoId) {
        const toBeRemovedIndex = this.todos.findIndex(todo => todo.id === todoId);
        this.todos.splice(toBeRemovedIndex, 1);
    }
}
