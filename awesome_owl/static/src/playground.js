/** @odoo-module **/

import { Component, markup, useState} from "@odoo/owl";
import { Counter } from "./counter/counter";
import { Card } from "./card/card";
import { TodoList } from "./todo/todoList/todoList";

export class Playground extends Component {
    static template = "awesome_owl.playground";

    static components = { Counter, Card, TodoList };

    setup(){
        this.test1 = "<div><p>Some text</p></div>";
        this.test2 = markup("<div><p>Some text</p></div>");
        this.sum = useState({value:0});
    }

    incrSum(){
        this.sum.value++;
    }
}
