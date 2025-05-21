/** @odoo-module **/

import {Counter} from "./counter/counter";
import {Card} from "./card/card";
import {TodoList} from "./todo_list/todo_list";

import {Component, markup, useState} from "@odoo/owl";

export class Playground extends Component {
    static template = "awesome_owl.playground"
    static components = {Counter, Card, TodoList};

    cardHtmlContent = markup("<a href='://odoo.com'>some text 2</a>");

    setup() {
        this.state = useState({sum: 0});
    }

    incrementSum() {
        this.state.sum++;
    }


}
