import { Component, useState, useRef, onMounted } from "@odoo/owl";
import { TodoItem } from "./todo_item";

export class TodoList extends Component {
    static template = "awesome_owl.todo_list";
    static components = { TodoItem };

    setup() {
        this.todos = useState([
            {id: -1, description: "sample", isCompleted: false},
            {id: -2, description: "sample", isCompleted: true},
            {id: -3, description: "sample", isCompleted: false},
        ]);
        this.inputRef = useRef("input");
        this.todoIdCounter = 1;
        
        onMounted(() => this.inputRef.el.focus());
    }

    addTodo = (ev) => {
        if (ev.key === 'Enter') {
            this.todos.push({
                id: this.todoIdCounter++,
                description: ev.target.value,
                isCompleted: false,
            });
            ev.target.value = "";
        }
    }

    toggleState = () => {  }
    

    removeTodo = (id) => {
        const index = this.todos.findIndex((t) => t.id === id);
        if (index >= 0) this.todos.splice(index, 1);
    }
}
