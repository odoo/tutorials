import { Component, useState, useRef, onMounted } from "@odoo/owl";
import { TodoItem } from "../todo_item/todo_item";
export class TodoList extends Component {
    static template = "awesome_owl.todo_list";
    static components = { TodoItem };

    setup() {
        this.todoListRef = useRef("todo_list");
        this.todoInputRef = useRef("new_todo_input");
        onMounted(() => {
            this.todoInputRef.el.focus();
        });
        this.state = useState({
            todos: [
            ],
            newTodoText: "",
        });
    }
    addTodo() {
        if (this.state.newTodoText.trim() === "") {
            return;
        }
        const newTodo = {
            id: Date.now(),
            text: this.state.newTodoText,
            isCompleted: false,
        };
        this.state.todos.push(newTodo);
        this.state.newTodoText = "";
        this.todoListRef.el.style.backgroundColor = 'white';
    }
    toggleTodo(todoId) {
        const todo = this.state.todos.find(t => t.id === todoId);
        if (todo) {
            todo.isCompleted = !todo.isCompleted;
        }
        //change the color of the list
        this.todoListRef.el.style.backgroundColor = this.state.todos.every(t => t.isCompleted) ? 'lightgreen' : 'white';
    }
    onRemoveTodo(todoId) {
        this.state.todos = this.state.todos.filter(t => t.id !== todoId);
        //change the color of the list
        this.todoListRef.el.style.backgroundColor = (this.state.todos.every(t => t.isCompleted) && this.state.todos.length > 0) ? 'lightgreen' : 'white';
    }
}