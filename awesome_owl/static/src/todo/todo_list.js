/** @odoo-module **/

import { Component, useState , useRef, onMounted } from "@odoo/owl";
import { TodoItem } from "./todo_item";

export class TodoList extends Component {

    static components = { TodoItem};

    static template = "awesome_owl.Todo_list"

    static props = {};

    setup() {
        this.todos = useState([]);
        this.next_id = 0;
        this.input = useRef("keyboard_input");
        onMounted(() => {
            this.input.el.focus();
        });
    }

    addTodo(ev) {
        if (ev.keyCode === 13 && ev.target.value !== "") {
            this.todos.push({ id: this.next_id,description: ev.target.value, isCompleted: false });
            ev.target.value = "";
            this.next_id++
        }
    }

    // Call the method to change the value of the isCompleted
    toggleCompletionByID(todo_item_id) {

        // Finds the to-do with the ID matching the TodoItem that triggered the callback
        const todo = this.todos.find(t => t.id === todo_item_id);
        if (todo) {
            todo.isCompleted = !todo.isCompleted;
        }
    }

    rmTodoByID(todo_item_id) {
        // Finds the to-do with the ID matching the TodoItem that triggered the callback
        const todo_index = this.todos.findIndex(t => t.id === todo_item_id);
        if (todo_index !== -1) {
            this.todos.splice(todo_index, 1);
        }
    }
}
