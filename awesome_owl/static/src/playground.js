/** @odoo-module **/

import { markup, Component, useState } from "@odoo/owl";
import { Counter } from "./counter/counter";
import { Card } from "./card/card";
import { TodoList } from "./todo/todo_list";

export class Playground extends Component {
    static template = "awesome_owl.playground";

    value1 = "<div class='text-primary'>Some content</div>"
    value2 = markup("<div class='text-primary'>Some content</div>")
    
    static components = { Counter, Card , TodoList };

    setup() {
        this.state = useState({ sum: 0 });
    }

    incrementSum() {
        this.state.sum++;
    }
}
