/** @odoo-module **/

import { useClicker } from "./clicker_hook";
import { Component } from "@odoo/owl";
import { humanNumber } from "@web/core/utils/numbers";

export class ClickerValue extends Component {
    static template = "awesome_clicker.clicker_value";
    static components = { humanNumber };
    static props = {};

    setup() {
        this.clickerHook = useClicker();
    }

    humanize(number) {
        // we need this function because otherwise 
        // humanNumber would not be recognised in the xml file
        if (number < 1000) {
            return humanNumber(number);
        }
        else {
            return humanNumber(number, {decimals: 2});
        }
    }
}