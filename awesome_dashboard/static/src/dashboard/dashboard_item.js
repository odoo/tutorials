import { Component, xml } from '@odoo/owl';

export class DashboardItem extends Component {
    static template = xml`
        <div class="card d-inline-block m-2" t-attf-style="width: {{18 * props.size}}rem">
            <div class="card-body">
                <t t-slot="default" />
            </div>
        </div>
    `;

    static props = {
        size: {
            type: Number,
            optional: true,
        },
        slots: {
            default: {}
        }
    };

    static defaultProps = {
        size: 1
    };
}
