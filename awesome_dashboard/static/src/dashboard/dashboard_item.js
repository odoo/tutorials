import { Component, xml, useState } from "@odoo/owl"

export class DashboardItem extends Component {
    static props = {
        slots: { type: Object, optional: true },
        size: { type: Number, optional: true },
        title: { type: String }
    }

    static defaultProps = { size: 1 }

    static template = xml`
        <div class="card d-inline-block m-2" t-attf-style="width: {{18 * props.size}}rem;">
            <div class="card-body d-flex flex-column justify-content-center">
                <h3 class="card-title text-center">
                    <t t-esc="props.title"/>
                </h3>
                <span class="fs-1 text-center text-primary">
                    <t t-slot="default"/>
                </span>
            </div>
        </div>
    `
}