import { Component, useState, useRef, onMounted } from "@odoo/owl";
import { TodoItem } from "./todo_item";

export class TodoList extends Component {
    static template = "awesome_owl.TodoList"

    setup() {
        this.todos = useState([ {
            id : 0,
            description : "Buy milk",
            isCompleted : false,
        } ]);
        this.inputRef = useRef('input_todo')
        onMounted(() => {
            this.inputRef.el.focus();
        })
    }

    static components = { TodoItem };

    addTodo(ev) {
        if (ev.keyCode == 13 && ev.target.value != "") {
            this.todos.push({ id: this.todos.length, description: ev.target.value, isCompleted: false});
            ev.target.value = "";
        }
        
    }

    toggleState(id) {
        const todo = this.todos.find((todo) => todo.id == id);
        if (todo) {
            todo.isCompleted = !todo.isCompleted;
        }
    }

    removeTodo(id) {
        let index = this.todos.findIndex((todo) => todo.id === id);
        if (index >= 0) {
            this.todos.splice(index, 1);
            this.todos.forEach(todo => {
                if (index < todo.id) {
                    todo.id = index;
                    index++;
                }
            });
        }
    }

}
