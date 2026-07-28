import { Component, markup, useState } from "@odoo/owl";
import { Counter } from "./counter/counter";
import { Card } from "./card/card";
import { TodoList } from "./todo/todo_list";

export class Playground extends Component {
    static props = [];
    static template = "awesome_owl.playground";
    static components = {
        Counter,
        Card,
        TodoList,
    };

    content1 = markup("<b>This is the content for card 1</b>");

    setup() {
        super.setup();
        this.state = useState({
            total: 0,
        });
    }

    onCounterIncremeneted = () => {
        console.log(this.state)
        this.state.total ++;
    }
}
