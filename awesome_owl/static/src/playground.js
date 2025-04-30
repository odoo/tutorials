/** @odoo-module **/

import { Component, markup } from "@odoo/owl";
import { Counter } from './Counter/counter';
import { Card } from './Card/card';

export class Playground extends Component {
    static template = "awesome_owl.playground";

    html = markup("<div>some content</div>")

    static components = { Card };
}
