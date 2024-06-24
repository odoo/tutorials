/** @odoo-module **/

import { registry } from "@web/core/registry";
import { Component, useState } from "@odoo/owl";
import { useService } from "@web/core/utils/hooks";

export class ClientAction extends Component {
    static template = "awesome_clicker.ActionButton";
    static props = {
        description: { type: String, optional: true },
        action: Object,
        actionId: { type: Number, optional: true }
    };

    setup() {
        this.clickerService = useState(useService("awesome_clicker.clickCounter"));
    }

    incrementButtonAction() {
        this.clickerService.increment(9);
    }
}

registry.category("actions").add("awesome_clicker.client_action", ClientAction);