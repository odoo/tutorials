import {Component, useState, useRef, onMounted} from '@odoo/owl'
import {TodoItem} from "./todo_item";
import {useAutofocus} from "../utils";

export class TodoList extends Component {
    static template = "awesome_owl.todo_list";
    static props = {};

    setup() {
        this.state = useState({
            todos: [],
            ids: 1
        })
        useAutofocus("input");

        this.addTodo = this.addTodo.bind(this);
        this.toggleCompleted = this.toggleCompleted.bind(this);
        this.deleteTodo = this.deleteTodo.bind(this);
    }

    addTodo(event) {
        if (event.keyCode === 13) {
            this.state.todos.push({id: this.state.ids, description: event.target.value, isCompleted: false});
            this.state.ids++;
            event.target.value = "";
        }
    }

    toggleCompleted(todo_id){
        const todo_pos = this.findTodo(todo_id);
        if (todo_pos < 0) return;
        const todo = this.state.todos[todo_pos]
        todo.isCompleted = !todo.isCompleted;
    }

    deleteTodo(todo_id){
        const todo_pos = this.findTodo(todo_id);
        if (todo_pos < 0) return
        this.state.todos.splice(todo_pos, 1);
    }

    findTodo(todo_id){
        let i = 0;
        const num_todos = this.state.todos.length;
        while (i < num_todos && this.state.todos[i].id !== todo_id) i += 1;
        if (i === num_todos) return -1;

        return i;
    }

    static components = {TodoItem};
}