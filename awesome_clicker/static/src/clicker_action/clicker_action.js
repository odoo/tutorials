import { Component, useState } from "@odoo/owl";
import { registry } from "@web/core/registry";
import { useService } from "@web/core/utils/hooks";

export class ClickerAction extends Component {
    static template = "awesome_clicker.clicker_action";

    setup() {
        this.clickerService = useService("awesome_clicker.game_service");
        this.clickerState = useState(this.clickerService.state);
    }
}

registry.category("actions").add("awesome_clicker.clicker_action", ClickerAction);
