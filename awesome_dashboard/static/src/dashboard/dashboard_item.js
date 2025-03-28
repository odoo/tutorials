/** @odoo-module **/

import { Component } from "@odoo/owl";
import { _t } from "@web/core/l10n/translation";

export class DashboardItem extends Component {
    static template = "awesome_dashboard.DashboardItem";

    static props = {
        slots: {
            type: Object,
            shape: {
                default: Object
            },
        },
        size: {
            type: Number,
            default: 1,
            optional: true,
        },
    };
}
