import { Component, useState } from '@odoo/owl';
import { TodoItem } from './todo_item';
import { useAutoFocus } from '../utils';

export class TodoList extends Component {
    static template = 'awesome_owl.todo_list';
    static components = { TodoItem };
    static props = {};

    setup() {
        this.todos = useState([]);

        useAutoFocus('input');
    }

    addTodo(ev) {
        if (ev.keyCode === 13 && ev.target.value) {
            const lastTodo = this.todos.slice(-1)[0];
            this.todos.push({
                id: lastTodo === undefined ? 0 : lastTodo.id + 1,
                description: ev.target.value,
                isCompleted: false,
            });

            ev.target.value = '';
        }
    }

    removeTodo(elemId) {
        const index = this.todos.findIndex((elem) => elem.id === elemId);
        if (index >= 0) {
            this.todos.splice(index, 1);
        }
    }
}
