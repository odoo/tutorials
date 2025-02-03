/** @odoo-module **/

import { markup, Component, xml, useState } from "@odoo/owl";
import { Counter } from "./counter/counter";
import { Card } from "./card/card";
import { TodoList } from "./todo/todolist";
export class Playground extends Component {
    static template = "awesome_owl.playground";

    incrementSum = () => {
        this.state.sum++;
    }

    decrementSum = () => {
        this.state.sum--;
    }
    setup() {
        this.state = useState({
            sum: 0
        })
    }


    valueForMarkup = markup('<div class=\"text-danger\">Second World</div>')

    static components = { Card, Counter, TodoList };
}
