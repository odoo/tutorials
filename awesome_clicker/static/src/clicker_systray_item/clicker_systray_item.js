import { Component, useState, useExternalListener } from "@odoo/owl";
import { registry } from "@web/core/registry";
import { useService } from "@web/core/utils/hooks";
import { useClicker } from "../useClicker";
import { ClickValue } from "../click_value/ClickValue";

export class ClickerSystrayItem extends Component {
    static template = 'awesome_clicker.systray_item'
    static props = {}
    static components = {ClickValue}

    setup() {
        this.actionService = useService('action')
        this.clicker = useClicker()
    }

    openDialog() {
        this.actionService.doAction({
           type: "ir.actions.client",
           tag: "awesome_clicker.client_action",
           target: "new",
           name: "Clicker"
        })
    }
}

registry.category("systray").add("awesome_clicker.clicker", {
    Component: ClickerSystrayItem,
}, { sequence: 100 });