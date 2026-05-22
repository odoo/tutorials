import { Component, useState, useRef, onMounted } from "@odoo/owl";
import { TodoItem } from "./todo_item";

export class TodoList extends Component {
    static template = "awesome_owl.TodoList";
    static components = { TodoItem };

    setup() {
        this.todos = useState([]);
        this.nextId = 1;
        this.inputValue = useState({ text: "" });

        this.inputRef = useRef("input");

        onMounted(() => {
            this.inputRef.el.focus(); 
        });

    }
    addTodo(ev) {
        if (ev.keyCode != 13) return

        this.todos.push({
            id : this.nextId++,
            description : this.inputValue.text,
            isCompleted : false
        })
        this.inputValue.text = ""

        this.inputRef.el.focus(); 
    }

    toggleState(id){
        const todo = this.todos.find(t => t.id === id)
        if (todo) {
            todo.isCompleted = !todo.isCompleted
        }
    }

    removeTodo(id) {
        const index = this.todos.findIndex(t => t.id === id);
        if (index >= 0) {
            this.todos.splice(index,1);
        }

        if (this.todos.length === 0) {
            this.nextId = 1;
        }
    }
}