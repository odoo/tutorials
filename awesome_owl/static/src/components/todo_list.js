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
                <p t-foreach="state.todos" t-as="todo" t-key="todo.id" >
                    <TodoItem todo="todo" toggleState.bind="toggleState" removeTodo.bind="removeTodo" />
                </p>
            </div>
        </div>
    `;

    setup() {
        this.state = useState( {todos: []});
        this.nextId = 0;

        useAutofocus("todoInput");
    }

    addTodo(ev){
        if (ev.keyCode === 13 && ev.target.value !== ""){
            this.state.todos.push({id: this.nextId, description: ev.target.value, isCompleted: false});
            this.nextId ++;
            ev.target.value = "";
            console.log(this.state.todos);
        }
    }

    toggleState(id, completed){
        for (let todo in this.state.todos) {
            if (todo.id === id){
                todo.isCompleted = completed;
            }
        }
    }

    removeTodo(id){
        console.log(this.state.todos);
        const index = this.state.todos.findIndex((todo) => todo.id === id);
        if (index >= 0) {
            // remove the element at index from list
            this.state.todos.splice(index, 1);
        }
    }
}
