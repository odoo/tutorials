/** @odoo-module **/

import { markup, Component, useState } from "@odoo/owl";
import { Counter } from "./counter/counter";
import { Card } from "./card/card";
import { TodoList } from "./todo/todo_list";

export class Playground extends Component {
    static template = "awesome_owl.playground";

    static components = { TodoList, Counter, Card };

    setup(){
        this.state = useState({
         card1: { title: "card 1", content: "content of card 1" },
         card2: { title: "card 2", content: "content of card 2" },
         sum: 2
        });

        this.content_value_escaped = "<div class='text-primary'>some content</div>";
        this.content_value = markup("<div class='text-primary'>some content</div>");
    }

    incrementSum(){
        this.state.sum++;
    }

}
