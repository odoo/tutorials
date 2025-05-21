/** @odoo-module **/

import { Component, markup, useState } from "@odoo/owl";
import { Counter } from "@awesome_owl/counter/counter";

export class Playground extends Component {
    static template = "awesome_owl.playground";
    static components = { Counter };

    setup() {
        this.extraContent1 = "Extra content 1";
        this.extraContent2 = markup("<strong>Extra content 2</strong>");

        this.state = useState({
            sum: 0,
        });
    }

    incrementSum() {
        this.state.sum++;
    }
}
