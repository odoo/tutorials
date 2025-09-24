import { Component, xml } from "@odoo/owl"

export class NumberCard extends Component{
    static template = xml`
        <p><t t-esc="props.title" /></p>
        <h1><b><t t-esc="props.value" /></b></h1>
    `
    static props = {
        title: [String], 
        value: [String, Number]
    }
}
