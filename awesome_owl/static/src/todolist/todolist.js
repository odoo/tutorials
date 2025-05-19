import { Component, useState, onMounted, useRef } from "@odoo/owl";
import { TodoItem } from "../todoitem/todoitem";
import { useAutofocus } from "../utils";

export class Todolist extends Component {
    static template = "awesome_owl.todolist";
    static components = { TodoItem };
    setup() {
        this.state = useState({
            todos: [],
            value: '',
            current_id: 0,
        });
        this.toggleState = this.toggleState.bind(this);
        this.removeTodo = this.removeTodo.bind(this);
        useAutofocus('inputRef');
    }
    
    removeTodo(id){
        const index = this.state.todos.findIndex((elem) => elem.id === id);
        if (index >= 0) {
            this.state.todos.splice(index, 1);
        }
    }

    toggleState(id) {
        if(this.state.todos){
            this.state.todos = this.state.todos.map(smth => {
                if(smth.id === id) {
                    smth.isCompleted = !smth.isCompleted;
                }
                return smth;
            });
        }
    }

    addTodo(ev) {
        if (ev.keyCode !== 13 || !this.state.value.trim()) {
            return;
        }
        this.state.todos.push({ id: this.state.current_id++, description: this.state.value, isCompleted: false });
        this.state.value = '';
    }
}

