import { Component, useState, markup } from "@odoo/owl";
import { Counter } from "./counter/counter"
import { Card } from "./card/card";

export class Playground extends Component {
    static template = "awesome_owl.Playground";
    static components = { Counter, Card };

    value1 = "<div class='text-primary'>test</div>";
    value2 = markup("<a href='odoo.com'>test2</a>");

    setup() {
    }

}
