/** @odoo-module **/

import { Component , markup } from "@odoo/owl";
import { Counter } from "./counter/counter";
import { Card } from "./card/card";  

export class Playground extends Component {
    static template = "awesome_owl.playground";
    static components = { Counter , Card };
    setup() {
        this.safeHTML = markup("<b>This is bold text</b>");  // Markup allows safe HTML
        this.unsafeText = "<i>This should not be italic</i>";  // This will be escaped
    }
}