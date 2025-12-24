import { Component, useExternalListener, useState } from "@odoo/owl";
import { registry } from "@web/core/registry";
import { useService } from "@web/core/utils/hooks";

export class ClickerMenu extends Component {
    static template = "awesome_clicker.clicker_menu";

    setup() {
        this.clickerService = useService("awesome_clicker.game_service");
        this.clickerState = useState(this.clickerService.state);
        this.action = useService("action");
        useExternalListener(document.body, "click", () => this.clickerService.increment(1));
    }

    doAction() {
        this.action.doAction({
            type: "ir.actions.client",
            tag: "awesome_clicker.clicker_action",
            target: "new",
            name: "Clicker Game",
        });
    }
}

export const systrayItem = {
    Component: ClickerMenu,
};

registry.category("systray").add("awesome_clicker.clicker_menu", systrayItem);
