import { Component, useState, useRef, onMounted } from "@odoo/owl";

import { TodoItem } from "./todo_item"; 


export class TodoList extends Component {
    static template = "awesome_owl.todo_list";
    static components = { TodoItem }; 

    setup() {
        this.todos = useState([]);
        this.state = useState({ counter_id : 0});
        this.inputRef = useRef('newTodoInput');
        onMounted(() => {
            this.inputRef.el.focus();
        })
    }

    addTodo(ev) {
        if (ev.keyCode === 13 && ev.target.value){
            const newTodo = {
                id : this.state.counter_id,
                description : ev.target.value,
                isCompleted : false,
            }
            this.state.counter_id++;
            this.todos.push(newTodo);
            ev.target.value = "";
        };
        
    }

    toggleTodoState(todoId) {
        const todo = this.todos.find(t=>t.id === todoId);
        if (todo) {
            todo.isCompleted = !todo.isCompleted;
        }
    }

    DeleteTodo(todoId) {
        const todoIndex = this.todos.findIndex(t=>t.id === todoId);
        if (todoIndex !== -1){
            this.todos.splice(todoIndex, 1)
        }
    }
}

