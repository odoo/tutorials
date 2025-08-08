/** @odoo-module **/

import { Component, markup, useState } from "@odoo/owl";
import { Card } from "./card/card";
import { Counter } from "./counter/counter";
import { TodoList } from "./todo/todo_list";

export class Playground extends Component {
    static template = "awesome_owl.playground";
    html = "<b class='text-primary'>This is html content</b>";
    html_markup = markup("<b class='text-primary'>This is html contetn with markup</b>");

    sum = useState({ total: 2 })

    onChange() {
        this.sum.total++;
    }

    static components = { Card, Counter,TodoList };
}
