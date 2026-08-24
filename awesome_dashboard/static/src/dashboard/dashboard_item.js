import { Component, xml } from "@odoo/owl"

export class DashboardItem extends Component {
    static props = {
        slots: { type: Object, optional: true },
        size: { type: Number, optional: true },
    }

    static defaultProps = { size: 1 }

    static template = xml`
        <div class="card d-inline-block m-2" t-attf-style="width: {{18 * props.size}}rem;">
            <div class="card-body d-flex flex-column justify-content-center">
                <t t-slot="default"/>
            </div>
        </div>
    `
}
