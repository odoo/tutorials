import { Component, xml } from "@odoo/owl";
import { registry } from "@web/core/registry";

export class VeryBasicComp extends Component {
    static props = {
        name: { type: String },
    };
    static template = xml`<p>Hi <t t-out="this.props.name"/></p>`;
}

registry.category("public_components").add("very_basic_comp", VeryBasicComp);
