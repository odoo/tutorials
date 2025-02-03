import { Component, useState, useRef, onMounted } from "@odoo/owl";
import { ToDoItem } from "./todo_item";

export class ToDoList extends Component {
    static template = "awesome_owl.todo_list";

    setup() {
        this.myRef = useRef('input_field');
        onMounted(() => {
            this.myRef.el.focus()
        });
        this.todos = useState([]);
        this.counter = 1;

    }

    addTodo(event) {
        if (event.keyCode === 13) {
            const input = event.target;
            const description = input.value.trim();

            if (description) {
                this.todos.push({
                    id: this.counter++,
                    description: description,
                    isCompleted: false
                });

                input.value = "";
            }
        }
    }

    removeTodo(todo_item) {
        const index = this.todos.findIndex((todos) => todos.id === todo_item.id);
        if (index >= 0) {
            this.todos.splice(index, 1);
        }
    }

    static components = { ToDoItem }

}       
