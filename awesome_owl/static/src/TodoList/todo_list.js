import { useRef, useState, Component } from '@odoo/owl';
import { TodoItem } from './todo_item';
import { useAutofocus } from '../utils';

export class TodoList extends Component {
    static template = 'awesome_owl.TodoList';

    setup() {
        this.todos = useState([]);
        this.state = useState({ id: 1 });

        this.inputRef = useRef('todo_input');
        useAutofocus("todo_input");
    }

    addTodo(ev) {
        if (ev.keyCode === 13 && ev.target.value.trim()) {
            this.todos.push({ id: this.state.id++, description: ev.target.value, isCompleted: false });
            ev.target.value = "";
        }
    }

    toggleState(todoId) {
        const todo = this.todos.find(todo => todo.id === todoId);
        if (todo){
            todo.isCompleted = !todo.isCompleted;
        }
    }

    static components = { TodoItem };
}
