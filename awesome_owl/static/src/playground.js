/** @odoo-module **/

import { Card } from "./card/card";
import { Component, markup, useState } from "@odoo/owl";
import { Counter } from "./counter/counter";


export class Playground extends Component {
    static template = "awesome_owl.playground";
    static components = {Card, Counter};

    sum = 0

    title = markup("<h1>Oh c'est un beau titre</h1>");
    content = markup("<div>C'est ma div</div>");
    context = useState({"title": this.title, "content": this.content, "sum": this.sum});

    incrementSum(){
        this.sum++;
        this.context.sum = this.sum;
    }
}