/** @odoo-module **/

import { Component, markup, useState } from "@odoo/owl";
import { Counter } from "./counter/counter";
import { Card } from "./card/card";
import { Todolist } from "./todo/todolist";

export class Playground extends Component {
    static template = "awesome_owl.playground";
    static components = { Counter, Card, Todolist };
    html = markup("<div> Hello Odooers </div>");
    
    setup() {
        this.state = useState({ val: 0 })
    }
    
    incrementSum() {
        this.state.val++;
    }

    decrementSum() {
        this.state.val--;
    }
}
