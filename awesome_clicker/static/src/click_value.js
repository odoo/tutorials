/** @odoo-module **/

import { Component } from "@odoo/owl";
import { humanNumber } from "@web/core/utils/numbers";
import { useClicker } from "./clicker_service";

export class ClickValue extends Component {
    static template = "awesome_clicker.ClickValue";

    setup() {
        this.clicker = useClicker();
    }

    formatted() {
        return humanNumber(this.clicker.clicks);
    }
}
