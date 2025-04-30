/** @odoo-module **/

import { markup, Component } from "@odoo/owl";

import { Counter } from "./counter/counter";
import { Card } from "./card/card";

export class Playground extends Component {
    static template = "awesome_owl.playground";
    static components = { Counter, Card };

    title_card_2 = "A not very beautiful card :(";
    content_card_2 = markup("<font color='green'>This one is not so rare...</font>");

    title_card_3 = "Basic card";
    content_card_3 = "<font color='blue'>This is not a basic card...</font>";
}
