import { browser } from "@web/core/browser/browser";
import { Component, useState, useRef, onMounted } from "@odoo/owl";
import { TodoItem } from "./todo_item";

export class TodoList extends Component {
    static template = "awesome_owl.todo_list";
    static components = { TodoItem };

    setup() {
        const localStoreTodos = JSON.parse(browser.localStorage.getItem("todos")) || [];

        this.todos = useState(localStoreTodos);
        this.nextId = this.todos.length + 1;
        this.inputRef = useRef("input");
        this.toggleTodo = this.toggleTodo.bind(this);
        this.deleteTodo = this.deleteTodo.bind(this);
        this.markAllCompleted = this.markAllCompleted.bind(this);
        this.clearAllTodo = this.clearAllTodo.bind(this);
        this.editTodo = this.editTodo.bind(this);
        this.saveTodo = this.saveTodo.bind(this);
        this.updateEditText = this.updateEditText.bind(this);
        this.deleteCount = 0;

        onMounted(() => {
            this.inputRef.el.focus();
        })
    }

    saveToLocalStorage() {
        browser.localStorage.setItem("todos", JSON.stringify(this.todos));
    }

    addTodo(ev){
        if (ev.keyCode === 13 && ev.target.value.trim() !== "") {
            const todoText = ev.target.value;
            if(this.todos.find((t) => t.description.toLowerCase() === todoText.toLowerCase())){
                ev.target.value = "";
                alert("Todo Already exits");
                return;
            }
            else{
                this.todos.push({
                id: this.nextId++,
                description: todoText,
                isCompleted: false,
                isEditing: false,
                editText: todoText,
            });
            }
            this.saveToLocalStorage();
            ev.target.value = "";
        }
    }

    toggleTodo(todoId) {
        const todo = this.todos.find((t) => t.id === todoId);
        if (todo) {
            todo.isCompleted = !todo.isCompleted;
            this.saveToLocalStorage();
        }
    }

    deleteTodo(todoId) {
        const index = this.todos.findIndex((t) => t.id === todoId);
        if (index >= 0) { 
            this.todos.splice(index, 1);
            this.saveToLocalStorage();
            this.deleteCount++;
        }
    }

    markAllCompleted() {
        this.todos.forEach((todo) => {
            todo.isCompleted = true;
        });
        this.saveToLocalStorage();
    }

    clearAllTodo() {
            this.todos.splice(0);
            this.saveToLocalStorage();
    }

    editTodo(todoId) {
        const edit = this.todos.find((t) => t.id===todoId);
        if(edit) {
            edit.editText = edit.description;
            edit.isEditing = true;
        }
    }

    saveTodo(todoId, newText) {
        const save =  this.todos.find((t) => t.id === todoId);
        if (save) {
            save.description = save.editText;
            save.isEditing = false;
            this.saveToLocalStorage();
        }
    }

    updateEditText(todoId, value) {
        const todo = this.todos.find((t) => t.id === todoId);
        if (todo) {
            todo.editText = value;
        }
    }
    get totalTodos () {
        return this.todos.length;
    }
    get pendingTodos() {
        return this.todos.filter((t) => !t.isCompleted).length;
    }

    get completedTodos() {
        return this.todos.filter((t) => t.isCompleted).length;
    }

    get deleteTodoCount() {
        return this.deleteCount;
    }
}
