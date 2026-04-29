import { Component, markup, useState} from "@odoo/owl";
import { Counter } from "./counter/counter";
import { Card } from "./card/card";

export class Playground extends Component {
    static template = "awesome_owl.playground";
    static components = { Counter, Card };
    html = markup("<p>This is some <strong>HTML</strong> content.</p>");

    setup() {
        this.state = useState({ incrementSum: 0 });
    }

    onCounterIncremented() {
        this.state.incrementSum++;
    }

}
