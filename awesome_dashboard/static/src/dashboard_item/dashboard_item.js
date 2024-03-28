/** @odoo-module **/

import { Component, xml, useRef } from "@odoo/owl";
//import { registry } from "@web/core/registry";

export class DashboardItem extends Component {
    //static template = "awesome_dashboard.dashboard_item";
    static props = { 
        slots: {
            type: Object,
            shape: {
                default: Object
            },
        },
        size: {
            type: Number,
            default: 1,
            optional: true,
        }
    }

    setup() {
        this.size = this.props.size !== undefined ? this.props.size : 1;
    }

    static template = xml`
    <div class="card m-2 border-dark" t-attf-style="width: {{18*size}}rem">
        <div class="card-body">
            <t t-slot="default"/>
            <div class="text-center font-weight-bold text-success">
                <t t-slot="highlight"/>
            </div>
        </div>

    </div>
    `;
    
}

//registry.category("actions").add("awesome_dashboard.dashboard_item", DashboardItem);
