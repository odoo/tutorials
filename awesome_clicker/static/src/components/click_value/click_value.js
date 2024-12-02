/** @odoo-module **/

import {Component} from "@odoo/owl";
import {humanNumber} from "@web/core/utils/numbers";


export class ClickValue extends Component {
    static template = "awesome_clicker.click_value";

    static props = {
        clicks: {
            type: Number
        }
    }

    hNum() {
        return humanNumber(this.props.clicks, {decimals: 1, minDigits: 1})
    }

    jsonClick() {
        return JSON.stringify({clicks: this.props.clicks})
    }
}
