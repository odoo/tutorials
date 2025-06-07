/** @odoo-module **/

import { Component, markup, useState } from "@odoo/owl";
import { Counter } from "./counter/counter.js";
import { Card } from "./card/card.js";
import { TodoList } from "./todo/todo_list.js";

export class Playground extends Component {
    static template = "awesome_owl.playground";
    static components = { Counter, Card, TodoList };

    raw_card_title = "<u>Hello</u>";
    raw_card_text = "<u>World</u>";

    card_title = markup(this.raw_card_title);
    card_text = markup(this.raw_card_text);

    setup() {
        this.state = useState({counter_sum: 2});
    }

    incrementSum() {
        this.state.counter_sum++;
    }
}
