/** @odoo-module **/

import {Component, markup, useState} from "@odoo/owl";
import {Counter} from "./counter/counter";
import {Card} from "./card/card";
import {TodoList} from "./todoList/todoList"

export class Playground extends Component {
    static template = "awesome_owl.playground";
    static components = {Counter, Card, TodoList};

    valueMarkup = markup("<u>MARKUP</u>")

    setup() {
        this.sum = useState({value: 2});
        this.incrementSum = this.incrementSum.bind(this);
    }

    incrementSum() {
        this.sum.value++;
    }
}
