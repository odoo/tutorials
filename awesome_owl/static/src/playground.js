import { markup, Component, useState } from "@odoo/owl";
import { Counter } from "./counter/counter";
import { Card } from "./card/card";

export class Playground extends Component {
    static template = "awesome_owl.playground";
    static components = { Counter, Card };

    setup() {
        this.normalString = "<div>This is escaped HTML</div>";
        this.htmlContent = markup("<div class='text-primary'>This is rendered as HTML</div>");
        this.state = useState({
            sum: 2,
        });
    }

    incrementSum() {
        this.state.sum++;
    }
}
