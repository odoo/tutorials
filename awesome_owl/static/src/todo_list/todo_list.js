/** @odoo-module **/
import { Component, useState, useRef, onMounted } from "@odoo/owl";
import { TodoItem } from "./todo_item";

export class TodoList extends Component {
    static template   = "awesome_owl.TodoList";
    static components = { TodoItem };

    setup() {
        this.todos     = useState([]);
        this.nextId    = 1;
        this.inputRef  = useRef("todoInput");
        this.deletedCount = useState({value: 0,});

        onMounted(() => {
            this.inputRef.el.focus();
        });
    }

    get totalTodos() {
    return this.todos.length;
    }

    get completedTodos() {
        return this.todos.filter((todo) => todo.isCompleted).length;
    }

    get pendingTodos() {
        return this.todos.filter((todo) => !todo.isCompleted).length;
    }

    addTodo(ev) {
        if (ev.keyCode === 13) {
            const description = ev.target.value.trim();
            const duplicate = this.todos.some((todo) => todo.description === description);
        if (duplicate)return;
            this.todos.push({
                id:          this.nextId++,
                description: description,
                isCompleted: false,
            });
            ev.target.value = "";
        }
    }

    toggleState(todoId) {
        const todo = this.todos.find(t => t.id === todoId);
        if (todo) {
            todo.isCompleted = !todo.isCompleted;
        }
    }

    removeTodo(todoId) {
        const index = this.todos.findIndex(t => t.id === todoId);
        if (index >= 0) {
            this.todos.splice(index, 1);
            this.deletedCount.value++;
        }
    }

    clearAll() {
        this.todos.splice(0, this.todos.length);
    }

    markAllRead() {
        for (const todo of this.todos) {
            todo.isCompleted = true;
        }
    }

}
