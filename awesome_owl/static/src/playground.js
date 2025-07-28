/** @odoo-module **/

import { Component, useState, markup } from "@odoo/owl";
import { Counter } from "./counter/counter";
import { Card } from "./card/card";
import { TodoList } from "./todo/todo_list";

export class Playground extends Component {
    static template = "awesome_owl.playground";
    static components = { Counter, Card, TodoList };
    static props = {};

    setup() {
        this.state = useState({ 
            counter1: 0,
            counter2: 0,
            counter3: 0,
        });
        
        // Properties needed by the template
        this.normalString = "This is normal text with <b>HTML tags</b>";
        this.markupString = markup("This is <em>markup</em> with <strong>HTML tags</strong>");
        this.dangerousMarkup = markup("This could be dangerous content");
        this.markup = markup;
    }

    get sum() {
        return this.state.counter1 + this.state.counter2;
    }

    updateCounter(counterName, value) {
        this.state[counterName] = value;
    }
}
