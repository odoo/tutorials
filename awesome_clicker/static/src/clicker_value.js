/** @odoo-module **/

import { Component } from "@odoo/owl";
import { useClicker } from "./clicker_hook";
import { humanNumber } from "@web/core/utils/numbers";

export class ClickerValue extends Component {
    static template = "awesome_clicker.ClickerValue";

    setup() {
        this.clicker_hook = useClicker();
    }

    humanDisplayMode() {
        return humanNumber(this.clicker_hook.state.clicks);
    }
}
