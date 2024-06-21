/** @odoo-module **/

import { Component, useState, useExternalListener, reactive } from "@odoo/owl";
import { _t } from "@web/core/l10n/translation";

import { useClicker } from "../clicker_hook";
import { formatFloat, humanNumber } from "@web/core/utils/numbers";

export class ClickValue extends Component {
    static template = "awesome_clicker.ClickValue";

    setup() {
        this.clicker = useClicker();
        console.log("🚀 ~ this.clicker:", this.clicker);

        // this.humanReadableClickValue = useState({
        //     value: humanNumber(this.clicker.state.clicks),
        // });

        // this.humanReadableClickValue = reactive(this.clicker.clicks, ());

        // console.log(this.humanReadableClickValue);
    }
    humanNumber(c) {
        return humanNumber(c);
    }
}
