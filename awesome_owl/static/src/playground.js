/** @odoo-module **/

import { Component, markup, useState, xml } from "@odoo/owl";
import { Counter } from "./Counter/counter";
import { Card } from "./card";
import { TodoList } from "./Todo/todo";

export class Playground extends Component {
    static template = xml`
    <div class="p-3">
    <t t-call="awesome_owl.playground"/>
        <Counter onChange.bind="incrementSum"/>
        <Counter onChange.bind="incrementSum"/>

        <Card title="'My Title 1'" content="htmlContent1"/>
            <Card title="'My Title 2'" content="htmlContent2"/>
            <TodoList/>
        </div>  
    `;

    static components = { Counter, Card, TodoList };

    setup() {
        this.htmlContent1 = markup("<div>Hello <b>World</b></div>");
        this.htmlContent2 = markup("<div class='text-primary'>Some italic content</div>");
        this.state = useState({ sum: 2 })
    }
    incrementSum(value) {
        this.state.sum++;
    }
}
