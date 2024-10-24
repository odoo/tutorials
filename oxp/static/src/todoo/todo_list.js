/** @odoo-module **/
import {Component, useState} from "@odoo/owl";
import {TodoItem} from "./todo_item";

export class TodoList extends Component {
    static template = "oxp.TodoList";
    static components = {TodoItem};
    static props = {
        name: String,
        list_id: Number,
        remove: Function,

    };

    static nID = 1;

    setup() {
        this.list = useState([]);
    }

    add_with_key(ev) {
        if (ev.keyCode === 13) {
            this._addTodo(ev.target);
        }
    }

    add_with_button() {
        let input = document.getElementById('input-add-task-'+this.props.list_id);
        this._addTodo(input);
    }

    _addTodo(input) {
        if (input.value.trim()) {
            this.list.push(
                {
                    id: TodoList.nID++,
                    desc: input.value.trim(),
                    isDone: false
                },
            );
        }
        input.value = ''
    }

    toggleTodo(id) {
        let todo = this.list.find(todo => todo.id === id);
        todo.isDone = !todo.isDone;
    }

    removeTodo(id) {
        this.list.splice(this.list.findIndex(todo => todo.id === id), 1);
    }

    remove() {
        this.props.remove(this.props.list_id);
    }
}
