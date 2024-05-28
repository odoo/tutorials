/** @odoo-module **/

import { Component, useState, useRef, onMounted } from "@odoo/owl";
import { TodoItem } from "./todo_item";

export class TodoList extends Component {
    static template = "awesome_owl.todo_list";
    static components = { TodoItem };

    setup() {
        this.todos = useState([]);
        this.uid = 0;
        this.inputfield = useRef('list-input');
        onMounted(() => {
            this.inputfield.el.focus();
        });
    }

    completeTodo(id) {
        var todo = this.todos.find(x => x.id === id);
        todo.isCompleted = !todo.isCompleted;
    }

    removeTodo(id){
        this.todos.splice(this.todos.findIndex((x) => x.id === id), 1);
    }

    addTodo(ev) {
        if (ev.keyCode === 13) {
            if (ev.target.value) {
                this.todos.push({
                    id: this.uid++,
                    description: ev.target.value,
                    isCompleted: false,
                });
                ev.target.value = ''
            }
        }
    }
}