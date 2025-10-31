import { Component } from "@odoo/owl";
import { useClicker } from "../clicker_hook";
import { humanNumber } from "@web/core/utils/numbers"

export class ClickValue extends Component {
    static template = "awesome_clicker.ClickValue";
    static props = {};

    setup() {
        this.clicker = useClicker()
    }

    get humanVal() {
        return humanNumber(this.clicker.count.clicks, {
            decimals: 1,
        });
    }
}
