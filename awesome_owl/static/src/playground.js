/** @odoo-module */

import { Component, useState, markup } from '@odoo/owl';
import { Card } from './Cards/cards';
import { Counter } from './Counter/counter';
import { TodoList } from './Todo/todo_list';

export class Playground extends Component {
    static template = "awesome_owl.Playground";
    static components = { Card, Counter, TodoList };
    static props = {}; 

    setup() {
        this.state = useState({ sum: 0 });

        this.cards = [
            { title: 'Card 1', content: markup('<div class="text-primary" style="color: black !important;">Content for card 1</div>') },
            { title: 'Card 2', content: markup('<div class="text-primary" style="color: black !important;">Content for card 2</div>') },
        ];
    }

    incrementSum = (value) => {
        this.state.sum += value;
    }

    addTodo = (description) => {
        if (description.trim()) {
            this.todos.push({
                id: this.nextId++,
                description,
                isCompleted: false,
            });
        }
    };
}
