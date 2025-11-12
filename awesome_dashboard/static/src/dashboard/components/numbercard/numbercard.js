import { Component, xml } from "@odoo/owl";

export class NumberCard extends Component{
    static template = xml`
        <div class="dashboard-number-class">
            <h3><t t-esc="props.title"/></h3>
            <h1 class="text-center text-success" t-esc="props.number"/>
        </div>
    `;

    static props = {
        title : String,
        number : Number,
    };    
}
