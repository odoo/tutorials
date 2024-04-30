/** @odoo-module **/

import { registry } from "@web/core/registry";
import { Component, useState } from "@odoo/owl";
import { useService } from "@web/core/utils/hooks";

class ClientAction extends Component {
    static template = "awesome_clicker.ClientAction"
    
    setup(){
        this.clickerService  = useState(useService('clicker_service'))
    }

}

registry.category("actions").add("awesome_clicker.client_action", ClientAction);