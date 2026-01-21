import { Component, onMounted, useRef, useState } from "@odoo/owl";

import { TodoItem } from "./todo_item"


export class TodoList extends Component {
    static template = "my_module.TodoList";
    static components = { TodoItem };

    setup() {
        this.state = useState({ todos: [] });
        this.taskCounter = 0;

        this.inputRef = useRef('todo_list_input');
        onMounted(() => {
            this.inputRef.el.focus();
        });
    }

    addTodo(ev) {
        if (ev.keyCode === 13 && ev.srcElement.value != "") {
            this.state.todos.push({id: this.taskCounter++, description: ev.srcElement.value, isCompleted: false});
            ev.srcElement.value = "";
        }
    }

    toggleTaskCompletion(toggled_item_id) {
        var toggled_item = this.state.todos.find(todo_item => todo_item.id === toggled_item_id);
        toggled_item.isCompleted = !toggled_item.isCompleted;
    }

    removeTask(task_id) {
        const removal_index = this.state.todos.findIndex((todo_item) => todo_item.id === task_id);
        if (removal_index >= 0) {
            this.state.todos.splice(removal_index, 1);
        }
    }
}
