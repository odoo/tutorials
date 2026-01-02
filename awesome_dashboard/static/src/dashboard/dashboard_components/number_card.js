import { Component, xml } from "@odoo/owl";

export class NumberCard extends Component {
    static props = {
        title: { type: String },
        value: { type: Object },
    };
    static template = xml`
        <t t-name="awesome_dashboard.NumberCard">
            <t t-esc="props.title"/> 
            <br/>
            <t t-esc="props.value"/>
        </t>
    `
}
