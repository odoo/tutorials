/** @odoo-module **/

import { Component, useState, useExternalListener } from "@odoo/owl";
import { _t } from "@web/core/l10n/translation";
import { registry } from "@web/core/registry";
import { useService } from "@web/core/utils/hooks";
import { useClicker } from "../clicker_hook";
import { ClickValue } from "../click_value/click_value";

export class ClientAction extends Component {
    static template = "awesome_clicker.ClientAction";
    static components = { ClickValue };

    setup() {
        this.clicker = useClicker();
    }
}

registry.category("actions").add("awesome_clicker.client_action", ClientAction);
