import { Component, useState, useRef, onMounted } from "@odoo/owl";
import { TodoItem } from "./todo_item";


export class TodoList extends Component {
    static props = [];
    static components = {TodoItem};
    static template = "awesome_owl.todo_list"

    setup(){
        this.todos = useState([
            { id: 1, description: "go running", isCompleted: true },
            { id: 2, description: "write tutorial", isCompleted: false },
            { id: 3, description: "buy milk", isCompleted: false },
        ]);

        this.inputRef = useRef('input');
        onMounted(() => { this.inputRef.el.focus() });
    }

    addTodo(ev){
        if (ev.key === "Enter" && ev.target.value.trim() !== ""){
            this.todos.push({
                id: this.todos.length + 1,
                description: ev.target.value.trim(),
                isCompleted: false
            });
            ev.target.value = ""
        }
    }

    setCompleted(id){
        const todo = this.todos.find(t => t.id === id);
        if (todo) {
            todo.isCompleted = !todo.isCompleted;
        }
    }

    deleteTodo(id){
        const idx = this.todos.findIndex(t => t.id === id);
        this.todos.splice(idx, 1);
    }
}
