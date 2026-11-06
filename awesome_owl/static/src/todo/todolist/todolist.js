import {Component, onMounted, useState, useRef} from "@odoo/owl";
import {TodoItem} from "../todoitem/todoitem";

export class TodoList extends Component {
    static template = 'awesome_owl.todolist';
    static props = {};
    static components = {TodoItem};

    setup() {
        this.todos = useState([
            {id: 1, description: 'complete js', isCompleted: false},
            {id: 2, description: 'commit it', isCompleted: true},
            {id: 3, description: 'push it on github', isCompleted: false}
        ]);
        this.myRef = useRef('taskInput');
        onMounted(() => {
            this.myRef.el?.focus();
        });
    }

    addTodo(e) {
        if (e.keyCode === 13) {
            if (e.target.value) {
                this.todos.push({
                    id: this.todos.length + 1,
                    description: e.target.value.trim(),
                    isCompleted: false
                });
                e.target.value = '';
            }
        }
    }

    toggleTodo(todoId) {
        const findtodo = this.todos.find((todo) => todo.id === todoId);
        if (findtodo) {
            findtodo.isCompleted = !findtodo.isCompleted;
        }
    }

    deleteTodo(todoId) {
        const todoIndex = this.todos.findIndex((todo) => todo.id === todoId);
        if (todoIndex !== -1) {
            this.todos.splice(todoIndex, 1);
        }
    }
}
