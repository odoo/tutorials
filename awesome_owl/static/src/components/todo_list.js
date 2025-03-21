import { TodoItem } from "./todo_item";
import { useAutofocus } from "../utilis"

import { Component, useState, xml, useRef, onMounted } from "@odoo/owl";

export class TodoList extends Component {
    static components = { TodoItem };

    static template = xml`
        <div class="p-3">
            <div>
                <input type="text" t-on-keyup="addTodo" placeholder="Add a todo" t-ref="todoInput"/> <br/>
            </div>
            <div>
                <p t-foreach="todos" t-as="todo" t-key="todo.id" >
                    <TodoItem todo="todo" toggleState.bind="toggleState" removeTodo="removeTodo" />
                </p>
            </div>
        </div>
    `;

    setup() {
        this.todos = useState([]);
        this.nextId = 0;

        useAutofocus("todoInput");
    }

    addTodo(ev){
        if (ev.keyCode === 13 && ev.target.value !== ""){
            this.todos.push({id: this.nextId, description: ev.target.value, isCompleted: false});
            this.nextId ++;
            ev.target.value = "";
        }
    }

    toggleState(id, completed){
        for (let todo in this.todos) {
            if (todo.id === id){
                todo.isCompleted = completed;
            }
        }
    }

    removeTodo(id){
        // const index = this.todos.findIndex((elem) => elem.id === id);

        // if (index >= 0) {
        //     // remove the element at index from list
        //     this.todos.findIndex.splice(index, 1);
        // }
    }
}
