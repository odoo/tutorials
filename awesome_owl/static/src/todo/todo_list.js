import {Component, useState} from "@odoo/owl";
import {TodoItem} from "./todo_item";
import {Todo} from "./todo_model";
import {useAutoFocus} from "../utils";


export class TodoList extends Component {
    static template = "awesome_owl.todo_list";
    static components = {TodoItem};

    index = 0;
    state = useState({todos: []});

    setup() {
        useAutoFocus('addTaskInput')
        this.toggleStateBind = this.toggleState.bind(this);
        this.removeTodoBind = this.removeTodo.bind(this);
    }

    keyUpAddTodo(ev) {
        if (ev.keyCode === 13 && ev.target.value !== "") {
            this.state.todos.push(new Todo(this.index + 1, ev.target.value, false));
            this.index++;
            ev.target.value = "";
        }
    }

    toggleState(id) {
        this.state.todos.forEach((value, index, arr) => {
            if (value.id === id) {
                value.toggle();
            }
        })
    }

    removeTodo(id) {
        const index = this.state.todos.findIndex((todo) => todo.id === id);
        if (index >= 0) {
            this.state.todos.splice(index, 1);
        }
    }
}
