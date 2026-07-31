import { Component, markup } from "@odoo/owl";
import { Card } from "./card/card";
import { Counter } from "./counter/counter";


export class Playground extends Component {
    static template = "awesome_owl.playground";

    static components = { Card, Counter };

    static props = {};

    get htmlContent() {
        return markup("<strong>This is bold</strong>");
    }

    get rawHtmlContent() {
        return "<strong>This is not bold</strong>";
    }
}
