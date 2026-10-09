import {Component, markup} from "@odoo/owl";
import {Counter} from "./counter/counter"
import {Card} from "./card/card"

export class Playground extends Component {
    static template = "awesome_owl.playground";
    static components = {Counter, Card}

    setup() {
        this.safeHtml = markup("<div class='text-success fw-bold'>some content</div>");
        this.withoutMarkup = "<div class='text-danger'>without markup</div>"
    }
}
