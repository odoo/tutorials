import { Component, useState, useRef, onMounted} from '@odoo/owl';
import { TodoItem } from '@awesome_owl/todo/todo_item';
import {useAutofocus} from '@awesome_owl/utils'


export class TodoList extends Component {
    static template = 'awesome_owl.TodoList';
    static components = { TodoItem }

    setup() {
        this.todos = useState([])
        this.Id = 1    
        useAutofocus('input');
    }

    addTodo(ev) {

        if (ev.keyCode === 13) {
            const description = ev.target.value.trim();

            if (description !== '') {
                this.todos.push({
                    id: this.Id++ ,
                    description: description,
                    isCompleted: false,
                });

                ev.target.value = '';
            }
        }
    }

    toggleTodo(todoId) {
        const todo = this.todos.find((t) => t.id === todoId);
        console.log(todo)
        if (todo) {
            todo.isCompleted = !todo.isCompleted;
        }
    }

    removeItemFromList(todoId) {
        const index = this.todos.findIndex((t) => t.id === todoId);

        if (index >= 0) {
            this.todos.splice(index, 1)
        }
    }
}