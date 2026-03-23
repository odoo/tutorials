import { Component, useState, useRef, onMounted } from "@odoo/owl";
import { TodoItem } from "./todo_item";

export class TodoList extends Component {
    static template = "awesome_owl.TodoList";
    static components = { TodoItem };
    
    addTodo(ev) {
        if (ev.keyCode !== 13 || ev.target.value.length === 0) {
            return
        }
        this.todos.push({
            id: this.count,
            description: ev.target.value,
            isCompleted: false
        });
        this.count++;
    }

    setup() {
        this.todos = useState([]);
        this.count = 1;
        this.todoRef = useRef("todo_input")
        onMounted(() => {
            this.todoRef.el.focus();
        });
    }

    toggleTodoItem(id) {
        const todoItem = this.todos.find(todo => {
            return todo.id === id
        });
        todoItem.isCompleted = !todoItem.isCompleted;
    }

    deleteTodoItem(id) {
        const todoItemIndex = this.todos.findIndex((todo) => todo.id === id);
        this.todos.splice(todoItemIndex, 1)
    }
}
