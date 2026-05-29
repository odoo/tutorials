import { markup, Component, useState } from "@odoo/owl";
import { Counter } from './counter/counter';
import { Card } from './card/card';
import { TodoList } from './todo/todolist';

export class Playground extends Component {
    static template = "awesome_owl.Playground";

    static components = { Counter, Card, TodoList};

    setup() {
        this.state = useState({ sum: 0 });
    }
    
    incrementSum() {
        this.state.sum++;
    }

    html_card_1 = "<u>Test Test Test Test Test Test Test Test Test</u>";
    html_card_2 = markup("<u>Test Test Test Test Test Test Test Test Test</u>");
}
