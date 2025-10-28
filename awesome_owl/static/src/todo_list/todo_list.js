import {onMounted, useRef, useState, Component} from "@odoo/owl"
import {TodoItem} from "./todo_item";
import {useAutofocus} from "../utils";

export class TodoList extends Component {
    static template = "awesome_owl.todo.list";

    static components = {TodoItem};

    static idGen = 0;

    static get id() {
        return this.idGen++;
    }

    setup() {
        this.todos = useState([]);
        useAutofocus('todo_input');
        this.toggleTodo = this.toggleTodo.bind(this);
        this.deleteTodo = this.deleteTodo.bind(this);
    }

    addTodo(ev) {
        if (ev.keyCode === 13 && ev.target.value) {
            this.todos.push({id: this.constructor.id, description: ev.target.value, isCompleted: false});
            ev.target.value = '';
        }
    }

    toggleTodo(id) {
        const index = this.todos.findIndex((elem) => elem.id === id);
        if(index !== -1) {
            this.todos[index].isCompleted = !this.todos[index].isCompleted;
        }
    }

    deleteTodo(id) {
        const index = this.todos.findIndex((elem) => elem.id === id);
        if(index !== -1) {
            this.todos.splice(index, 1);
        }
    }
}
