/** @odoo-module **/

import { Component, markup, useState } from "@odoo/owl";
import { Counter } from "./counter/counter";
import { Card } from "./card/card";
import { TodoList } from "./todo_list/todo_list";

export class Playground extends Component {
    static template = "awesome_owl.playground";

    static components = { Counter, Card, TodoList };

    setup() {
        // this.card1_content = "<div class='text-primary'>some content</div>";
        // this.card2_content = markup(
        //     "<div class='text-primary'>some content</div>"
        // );
        this.state = useState({
            sum: 0,
        });
    }

    incrementSum = () => {
        this.state.sum += 1;
    };
}
