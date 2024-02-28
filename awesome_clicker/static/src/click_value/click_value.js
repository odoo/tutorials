/** @odoo-module **/

import { Component } from "@odoo/owl";
import { useClicker } from "../use_clicker";
import { humanNumber } from "@web/core/utils/numbers";

export class ClickValue extends Component {
    static template = "awesome_clicker.ClickValue";
    static props = [];


    setup() {
        this.clicker = useClicker();
        this.humanNumber = humanNumber;
    }

}
