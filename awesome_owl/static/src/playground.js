/** @odoo-module **/

import { Component, markup, useState } from "@odoo/owl";
import { Counter } from "./counter/counter"
import { Card } from "./card/card";
import { TodoList } from "./todo/todo_list";


export class Playground extends Component {
    static template = "awesome_owl.playground";
    static components = { Card, Counter, TodoList };

    card_1_content = "<em>Card 1 content from the JS file </em>";
    card_2_content = markup("<em>Card 2 content from the JS file </em>");

    setup() {
        this.state = useState({ value: 2 });
    }

    incrementSum(){
        this.state.value++;
    }
}
