import { Component, useState } from "@odoo/owl";
import { registry } from "@web/core/registry";
import { useService } from "@web/core/utils/hooks";
import { ClickValue } from "../click_value/click_value";
import { Notebook } from "@web/core/notebook/notebook";

class ClientAction extends Component {
    static template = "awesome_clicker.client_action";
    static components = { ClickValue, Notebook};
    static props = ['*'];

    setup()
    {
        this.clicker = useService("awesome_clicker.clicker_service");
    }

    onClick()
    {
       this.clicker.addClicks(9);
    }

}
registry.category("actions").add("awesome_clicker.client_action",ClientAction)
