import { Component, useState } from "@odoo/owl";

import { registry } from "@web/core/registry";
import { useService } from "@web/core/utils/hooks";

export class ClientAction extends Component {
    static template = "awesome_clicker.client_action";

    setup() {
        this.clicker = useState(useService("awesome_clicker.cliker_service"))
    }
}

registry.category("actions").add("awesome_clicker.client_action", ClientAction);
