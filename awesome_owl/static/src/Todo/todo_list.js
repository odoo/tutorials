/** @odoo-module **/

import { Component, useRef, onMounted } from '@odoo/owl';
import { TodoItem } from './todo_item.js';

export class TodoList extends Component {
    static template = "awesome_owl.TodoList";
    static components = { TodoItem};

    static props = {
        todos: { type: Array },
        onAddTodo: { type: Function },
        removeTodo: { type: Function },
    };

    setup() {
        this.inputRef = useRef('todoInput');
        onMounted(() => {
                this.inputRef.el.focus()
        });
    }
}
