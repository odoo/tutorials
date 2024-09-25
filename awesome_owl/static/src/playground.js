/** @odoo-module **/

import { markup, Component, useState } from "@odoo/owl";
import { Counter } from "./counter/counter";
import { Card } from "./card/card";
import { TodoList } from "./todo/todo_list";

export class Playground extends Component {
    static template = "awesome_owl.playground";
    static components = {Counter, Card, TodoList};

    value1 = "<div>Text</div>";
    value2 = markup("<a href='https://github.com/odoo/owl/blob/master/doc/reference/templates.md#outputting-data' target='_blank'>Click Me</a>");

    setup (){
        this.state = useState({ totalSum:0 });
    }

    incrementTotalSum (){
        this.state.totalSum += 1;
    }
}
