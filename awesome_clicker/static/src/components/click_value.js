import { Component, xml } from "@odoo/owl";
import { humanNumber } from "@web/core/utils/numbers";
import { useClicker } from "./clicker_hook";

export class ClickValue extends Component {
    static props = {};
    static template = xml`  
        <t t-out="humanNumber(this.clicks.clicks, {decimals: 1})" t-att-data-tooltip='this.clicks.clicks'/>
    `;
    humanNumber = humanNumber;
    setup() {
        this.clicks = useClicker();
    }
}