/** @odoo-module **/

import { registry } from "@web/core/registry";
import { Component, useState } from "@odoo/owl";

class ClickerSystrayItem extends Component {
   static template = "awesome_clicker.ClickerSystrayItem" 

   setup (){
    this.state = useState({score: 0})
   }

   incrementScore(){
    this.state.score++;
   }
}

registry.category("systray").add("awesome_clicker.ClickerSystrayItem", {
    Component: ClickerSystrayItem,
});