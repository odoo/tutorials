/** @odoo-module **/

import { Counter } from "./counter/counter";
import { Card } from "./card/card";
import { markup, Component, useState } from "@odoo/owl";


export class Playground extends Component {
    static template = "awesome_owl.playground";


    setup() {
        this.state = useState({ value: 0 });
        this.html_normal = "<div class='text-primary'>some content</div>";
        this.html_markup = markup("<div class='text-primary'>some content</div>");
    }

    increment() {
        this.state.value++;
    }

    static components = { Card };
}
