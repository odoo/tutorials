import {Component, useState, xml} from "@odoo/owl";

export class DashboardItem extends Component {
    static template = xml`
        <div class="card d-inline-block m-2  flex-grow-1" t-attf-style="width: {{18* this.props.size}}rem">
        <div class="card-body">
           <p class="card-text">
            <t t-slot="default"/>
           </p>
        </div>
        </div>
    `
    static props = {
        size: {type: Number, optional: true},
        slots: {optional: true},
    }
    static defaultProps = {
        size: 1,
    };

}