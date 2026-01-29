import { Component, markup, useState} from "@odoo/owl";
import { Card } from "./card/card.js";
import { Counter } from "./counter/counter.js";
import { TodoList } from "./todo/todo_list.js";

export class Playground extends Component {
    static template = "awesome_owl.playground";
    static components = { Card, Counter, TodoList };
    
    setup() {
        this.state = useState({ sum: 0 });
        this.content1 = "<div>some text 1</div>";
        this.content2 = markup("<div>some text 2</div>");
    }

    incrementSum() {
        this.state.sum++;
    }
}
