/** @odoo-module **/

import { Component, useState, markup } from "@odoo/owl";
import { Counter } from "./counter/counter";
import { Card } from "./card/card";
import { ToDoList } from "./to_do/to_do_list";

export class Playground extends Component {
    static template = "awesome_owl.playground"

    setup(){
        this.state = useState({ sum: 0})
        this.incrementSum = this.incrementSum.bind(this);
    }

    incrementSum(){
        this.state.sum++
    }

    static components = { Counter, Card, ToDoList };
}
