import { Component, useState, useRef, onMounted } from "@odoo/owl";
import { TodoItem } from "../todo_item/todo_item"; 
import { useAutofocus } from "../../utils";

export class TodoList extends Component {
    static template = "awesome_owl.TodoList";
    static components = { TodoItem };

    setup() {
        this.todos = useState([]);
        this.nextId = 0;
        this.todoInputRef = useAutofocus("todoInput");
        // this.todoInputRef = useRef("todoInput");
        // onMounted(() => {
        //     if (this.todoInputRef.el) {
        //         this.todoInputRef.el.focus();  // Focus input
        //     }
        // });
    }

    addTodo(ev) {
        if (ev.keyCode === 13) {
            const input = this.todoInputRef.el;
            const description = input.value.trim();

            if (description) {
                this.todos.push({
                    id: this.nextId,
                    description: description,
                    isCompleted: false
                });
                input.value = "";  
                this.nextId++;
            }
        }
    }

    toggleState(todoId) {
        const todo = this.todos.find((todo) => todo.id === todoId);
        if (todo) {
            todo.isCompleted = !todo.isCompleted;
        }
    }

    removeTodo(taskId){
        const index = this.todos.findIndex((t) => t.id === taskId);

        this.todos.splice(index, 1);
    }
}
