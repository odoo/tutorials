/** @odoo-module **/

const { Component, useState, useRef, onMounted} = owl;
const { TodoItem } = require("../todoItem/todoItem");

export class TodoList extends Component {
    static template = "awesome_owl.todoList";
    static components = { TodoItem };

    setup = () => {
        this.todos = useState([])
        this.inputRef = useRef('todo_input');
        onMounted(() => {
            this.inputRef.el.focus(); 
        })
    }
    
    addTodo = (event) => {
        if (event.key === "Enter" && event.target.value) {
            this.todos.push({
                id: this.todos.length,
                description: event.target.value,
                isCompleted: false
            });
            event.target.value = '';
        }
    }

    toggleState = (todo) => {
        todo.isCompleted = !todo.isCompleted
    }

    removeTodo = (todo) => {
        this.todos.splice(this.todos.indexOf(todo), 1);
    }
}
