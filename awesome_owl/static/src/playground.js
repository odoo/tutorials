import { Card } from "./card/card";
import { Component, markup, useState } from "@odoo/owl";
import { Counter } from "./counter/counter";


export class Playground extends Component {
    static template = "awesome_owl.Playground";
    static components = { Card, Counter };
    static props = {
      heading: { type: String, optional: true }
    };

    setup() {
        this.str1 = "<div class='text-primary'>some content</div>";
        this.str2 = markup("<div class='text-primary'>HTML content using markup</div>");
        this.sum = useState({ value: 0 });
    }

    incrementSum() {
        this.sum.value++;
    }
}
