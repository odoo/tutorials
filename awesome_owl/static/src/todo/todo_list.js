/** @odoo-module **/
import { Component, useState} from "@odoo/owl";
import { TodoItem } from "./todo_item";
import { useAutofocus} from "../utils";


export class TodoList extends Component {
    static template = "awesome_owl.todo_list";
    static components = {TodoItem};
    setup(){
        this.todos = useState([]);
        this.counter = 1;
        useAutofocus("input");
    }

    addTodo(ev) {
        if (ev.key === "Enter") {
            const value = ev.target.value.trim();

            if (value) {
                console.log("Adding todo:", value);
                this.todos.push({"id":this.counter, "description": value, "isCompleted":false});
                this.counter += 1;
            }
            ev.target.value = '';

        }

    }

    toggleTodoState(id) {
        const todo = this.todos.find((t) => t.id === id);
        if (todo) {
        todo.isCompleted = !todo.isCompleted;
        }
     }

     removeTodo(elemId) {
        const index = this.todos.findIndex((elem) => elem.id === elemId);
        if (index >= 0) {
            // remove the element at index from list
            this.todos.splice(index, 1);
        }
     }

   
}
