import { Component, useState, xml, markup } from "@odoo/owl";

import { Counter } from './counter/counter';
import { Card } from './card/card';
import { TodoList } from './todo/todo_list';

export class Playground extends Component {
    setup() {
        this.state = useState({ 
            a: 0,
            b: 0,
            c: 0,
            content: markup(`<h1 class="text-danger">hello</h1>`),
            task_id: 1,
        })
        this.todos = useState([]);
    }

    increment_a() {
        this.state.a++
    }

    increment_b() {
        this.state.b++
    }

    increment_c() {
        this.state.c++
    }

    handleKeyup(ev) {
        const key = ev.key;

        if (key === "Enter" && ev.target.value) {
            this.todos.push({
                id: this.state.task_id,
                description: ev.target.value,
                isCompleted: false,
            })

            this.state.task_id++;
            ev.target.value = "";

            return;
        }
    }

    toggleTodo(id) {
        const idx = this.todos.findIndex(t => t.id === id);

        if (idx !== -1) {
            const old = this.todos[idx].isCompleted;
            this.todos[idx].isCompleted = !old;
        }
    }

    removeTodo(id) {
        const idx = this.todos.findIndex(t => t.id === id);


        if (idx !== -1) this.todos.splice(idx, 1);
    }

    static template = xml`
        <div>
            <Counter callback.bind="increment_a" />
            <Counter callback.bind="increment_b" />
        </div>
        
        <br />

        <div>
            <Card title="'Hola'">
                <Counter callback.bind="increment_c" />
            </Card>
        </div>

        <br />
        
        <div class="p-3">
            Sum:
            <t t-esc="state.a + state.b + state.c" />
        </div>

        <br />

        <input t-on-keyup="handleKeyup" />

        <div>
            <TodoList 
                list="todos" 
                toggleTodo.bind="toggleTodo"
                removeTodo.bind="removeTodo"
            />
        </div>
    `

    static components = { Counter, Card, TodoList }
}
