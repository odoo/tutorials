import { Component, xml } from "@odoo/owl";

export class DashboardItem extends Component {
    static props = {
        size: { type: Number, optional: true },
    };

    static template = xml`
        <div class="card d-inline-block m-2" t-attf-style="width: {{18 * (this.props.size | 1)}}rem">
            <t t-slot="default"/>
        </div>
    `
}