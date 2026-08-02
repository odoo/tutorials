import { Component, markup, useState } from "@odoo/owl";
import { Card } from "./card/card";
import { Counter } from "./counter/counter";


export class Playground extends Component {
    static template = "awesome_owl.playground";

    static components = { Card, Counter };
    static props = {};

    setup() {
        this.sum = useState({ value: 0 });
        this.onChange = this.onChange.bind(this);
    }

    get htmlContent() {
        return markup("<strong>This is bold</strong>");
    }

    get rawHtmlContent() {
        return "<strong>This is not bold</strong>";
    }

    onChange() {
        this.sum.value++;
    }
}
