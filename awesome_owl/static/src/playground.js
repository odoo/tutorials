/** @odoo-module **/

import { Component, useState, markup } from "@odoo/owl";
import { Counter } from "./counter/counter";
import { Card } from "./card/card";
import { TodoList  } from "./todolist/todo_list";

export class Playground extends Component {
    static template = "awesome_owl.playground";
    static components = { Counter, Card, TodoList };

    setup () {
        this.markup_text = markup("<p>Pink <i>fluffy u</i>nicorns");
        this.markup = markup;
        this.sum = useState({ value: 0 });
    }

    incrementSum() {
        this.sum.value++;
    }

    
}
