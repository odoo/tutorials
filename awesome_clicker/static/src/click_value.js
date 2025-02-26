import { Component, xml } from '@odoo/owl';
import { useClicker } from './utils';

export class ClickValue extends Component {
    static template = xml`
        <t t-if="props.label">Clicks: </t>
        <span
            t-att-data-tooltip="clicker.clicks">
            <t t-out="clicker.humanClicks"/>
        </span>
    `;
    static props = {
        label: {
            optional: true
        }
    };
    static defaultProps = {
        label: true
    };

    setup() {
        this.clicker = useClicker();
    }
};
