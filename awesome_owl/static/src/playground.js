import { Component, markup } from "@odoo/owl";
import { Counter } from "./counter";
import { Card } from "./card";

export class Playground extends Component {
    static template = "awesome_owl.playground";

    html = markup("<div class='text-primary'>some content</div>")
    static components = { Counter, Card }
    static props = {};
}
