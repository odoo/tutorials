import { Component, xml } from "@odoo/owl";
import { Card } from "./card"

export class NumberCard extends Component {
    static template = "awesome_dashboard.number_card";
    static components = { Card };
    static props = {
        title: String,
        value: Number
    };
    static template = xml`
        <t t-esc="props.title"/>
        <h1 style="color: var(--green);"><t t-esc="props.value"/></h1>
    `;
}
