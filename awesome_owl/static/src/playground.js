import { Component, useState, markup } from "@odoo/owl";
import { Counter } from "./counter/counter";
import { Card } from "./card/card";
import { TodoList } from "./todo/TodoList";

export class Playground extends Component {
    static template = "awesome_owl.playground";

    static components = { Counter, Card, TodoList };

    setup(){
        this.state = useState({sum: 2});
    }

    incrementSum(){
        this.state.sum++;
    }

    card1_value = "<div class = 'text-primary'>TESTINGINGINGING</div>";
    card2_value = markup("<div class = 'text-primary'>TESTINGINGINGING</div>");
}
