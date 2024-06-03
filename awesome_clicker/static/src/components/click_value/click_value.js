/** @odoo-module **/
import { Component, xml } from "@odoo/owl";
import { humanNumber } from "@web/core/utils/numbers";

export class ClickValue extends Component {
    static template = xml`
        <span t-attf-data-tooltip="{{props.value}}"><t t-esc="humanNumber(props.value)"/></span>
    `;

    setup() {
        this.humanNumber = humanNumber;
    }
}
