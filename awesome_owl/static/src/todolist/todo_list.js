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
        this.todos = useState([
            { id: 1, description: 'Learn JavaScript', isCompleted: true },
            { id: 2, description: 'Learn Odoo', isCompleted: false },
            { id: 3, description: 'Learn Owl', isCompleted: true },
            { id: 4, description: 'Learn React', isCompleted: false },
            { id: 5, description: 'Learn Vue', isCompleted: true },
            { id: 6, description: 'Learn Python', isCompleted: false },
        ]);
    }
}
