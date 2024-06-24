/** @odoo-module **/

import { Component } from "@odoo/owl";

import { useClicker } from "../clicker_hook";
import { humanNumber } from "@web/core/utils/numbers";

export class ClickValue extends Component {
    static template = "awesome_clicker.ClickValue";
    setup() {
        this.clicker = useClicker();
    }
    humanNumber(c) {
        return humanNumber(c);
    }
}
