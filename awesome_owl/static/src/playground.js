/** @odoo-module **/

import { Component, markup} from "@odoo/owl";

import { Counter } from "./counter";
import { Card } from "./card";


export class Playground extends Component {
    static template = "awesome_owl.playground";

    title = "<div style='color:blue'> Title </div>"
    content = "<div style='color:blue'> content </div>"

    safe_title = markup("<div style='color:blue'> Title </div>")
    safe_content = markup("<div style='color:blue'> content </div>")

    static components = { Counter, Card }
}
