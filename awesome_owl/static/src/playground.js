import { Component, markup } from "@odoo/owl";
import { Counter } from "./counter";
import { Card } from "./card";

export class Playground extends Component {
    static template = "awesome_owl.playground";
    static components = { Counter, Card };

    setup () {
        this.htmlContent = markup("<em style='color:red;'>red text</em>");
        this.normalString = "<b>no markup</b>";
    }
}
