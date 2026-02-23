import { Component, markup } from "@odoo/owl";
import { Card } from "./card/card";

export class Playground extends Component {
    static template = "awesome_owl.Playground";
    static components = { Card };

    setup() {
        this.htmlContent = "<b>This will not be rendered as bold</b>";
        this.safeHtmlContent = markup(
            "<b>This will be rendered as bold</b>"
        );
    }
}
