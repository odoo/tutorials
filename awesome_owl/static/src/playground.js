import {Component, markup, useState} from "@odoo/owl";
import {Counter} from "./counter/counter";
import {Card} from "./card/card";
import {Todo} from "./todo_list/todo";

export class Playground extends Component {
    static template = "awesome_owl.playground";

    static components = {
        Counter,
        Card,
        Todo,
    };

    setup() {
        this.htmlContent1 = markup("Some <strong>bold</strong> text content.");
        this.htmlContent2 = markup("<span class='text-primary'>Reusable</span> components are great!");

        this.counter = useState({
            value1: 0,
            value2: 0,
        });

        this.nextId = 4;

        this.todos = useState([
            {id: 1, description: "Buy milk", done: false},
            {id: 2, description: "Learn Owl Framework", done: true},
            {id: 3, description: "Write awesome code", done: false},
        ]);
    }

    resetCounters() {
        this.counter.value1 = 0;
        this.counter.value2 = 0;
    }

    addTodo(ev) {
        if (ev.keyCode === 13 && ev.target.value.trim() !== "") {
            this.todos.push({
                id: this.nextId++,
                description: ev.target.value,
                done: false,
            });

            ev.target.value = "";
        }
    }

    toggleTodo(todoId) {
        const todo = this.todos.find((t) => t.id === todoId);

        if (todo) {
            todo.done = !todo.done;
        }
    }
}