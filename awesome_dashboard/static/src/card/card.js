/** @odoo-module **/

import { Component, useState } from "@odoo/owl";

export class Card extends Component {
    static template = "awesome_dashboard.card";

    static props = {
        size: {type: Number, optional: true},
        slots: {type: Object, optional: true},
    };

    static defaultProps = {
        size: 1,
    };
}
