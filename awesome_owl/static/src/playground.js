import { Component, markup, useState } from "@odoo/owl";
import { Counter } from "./counter/counter";
import { Card } from "./card/card";

export class Playground extends Component {
    static template = "awesome_owl.playground";
    static components = { Counter, Card };

    setup () {
        this.htmlContent = markup("<em style='color:red;'>red text</em>");
        this.normalString = "<b>no markup</b>";
        this.state = useState({counter1: 0, counter2: 0});
    }

    get counterSum () {
        console.log(this.state.counter1, this.state.counter2);
        return this.state.counter1 + this.state.counter2;
    }

    updateCounter1 (count1) {
        this.state.counter1 = count1;
    }

    updateCounter2 (count2) {
        this.state.counter2 = count2;
    }
}
