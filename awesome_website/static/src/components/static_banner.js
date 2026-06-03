import { Component, xml } from "@odoo/owl";
import { registry } from "@web/core/registry";


export class StaticBanner extends Component {
    static template = xml`<h3 class="align-items-center">Hello, <t t-out="this.props.name"/>!</h3>`
    static props = {
        name: {
            type: String,
        },
    };
}

registry.category("public_components").add("static_banner", StaticBanner);
