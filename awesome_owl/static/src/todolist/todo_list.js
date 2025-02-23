import { Component, useState, useRef, onMounted } from '@odoo/owl';
import { TodoItem } from './todo_item';


export class TodoList extends Component {
    static template = 'awesome_owl.TodoList'
    static components = { TodoItem };
    setup() {
        this.state = useState({
            todos: [{ id: 1, description: 'Sample Task', isCompleted: false }],
            newTodo: ''
        });
        this.inputRef = useRef('input');
        onMounted(() => { this.inputRef.el.focus() });
        this.addNewTodo = this.addNewTodo.bind(this)
        this.deleteTodo = this.deleteTodo.bind(this) 
    }
    addNewTodo() {
        const newId = this.state.todos.length > 0 ? this.state.todos[this.state.todos.length - 1].id + 1 : 1
        this.state.todos.push({ id: newId, description: this.state.newTodo, isCompleted: false })
        this.state.newTodo = ''
    }
    deleteTodo(id) {this.state.todos = this.state.todos.filter((todo) => todo.id != id)}
    upperCaseAll() {
        this.state.todos = this.state.todos.map((todo) => {
            return { ...todo, description: todo.description.toUpperCase() }
        })
    }
}
