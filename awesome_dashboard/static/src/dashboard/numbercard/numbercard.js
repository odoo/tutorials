/** @odoo-module **/

import { Component } from "@odoo/owl";
import { _t } from "@web/core/l10n/translation";

export class NumberCard extends Component {
    static template = "awesome_dashboard.NumberCard";

    static props = {
        title: { type: String },
        value: { type: [String, Number] }
    }

    setup() {
        this._t = _t; 
    }
}
