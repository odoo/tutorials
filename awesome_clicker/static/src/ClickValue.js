import { Component } from "@odoo/owl";
import { humanNumber } from "@web/core/utils/numbers"

export class ClickValue extends Component {
    static template = "awesome_clicker.ClickValue";
    static props = {
        clicks: Number
    }

    setup() {
        this.humanize = (clicks) => {
            return humanNumber(clicks, {decimals: clicks > 1000 ? 1 : 0});
        }
    }
}
