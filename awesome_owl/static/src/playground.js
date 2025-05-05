/** @odoo-module **/

import { useState, markup, Component } from "@odoo/owl";

import { Counter } from "./counter/counter";
import { Card } from "./card/card";
import { TodoList } from "./todolist/todolist";

export class Playground extends Component {
    static template = "awesome_owl.playground";
    static components = { Counter, Card, TodoList };

    titleCard2 = "A not very beautiful card :(";
    contentCard2 = markup("<font color='green'>This one is not so rare...</font>");

    titleCard3 = "Basic card";
    contentCard3 = "<font color='blue'>This is not a basic card...</font>";

    setup() {
        this.state = useState({ sum: 2 });
    }

    incrementSum() {
        this.state.sum++;
    }
}
