import { Component, xml } from "@odoo/owl";
import { useClicker } from "./clicker_hook";

export class Tree extends Component {
    static props = {};
    static template = xml`
        <h1>Trees</h1>
        <div t-if="clicks.level >= 3">
            <div>
                <t t-esc="clicks.trees.pear"/>x 
                <span>pearTree (1x pear /30 seconds)</span>
                <i class="fa fa-tree"/>
            </div>
            <div>
                <button class="btn btn-primary" t-att-disabled="!(this.clicks.clicks>=1000000)" t-on-click="incrementPearTree">Buy pearTree (1000000 clicks)</button>
            </div>
        </div>
        <div t-if="clicks.level >= 3">
            <div>
                <t t-esc="clicks.trees.cherry"/>x 
                <span>cherryTree (1x cherry/30 seconds)</span>
                <i class="fa fa-tree"/>
            </div>
            <div>
                <button class="btn btn-primary" t-att-disabled="!(this.clicks.clicks>=1000000)" t-on-click="incrementCherryTree">Buy cherryTree(1000000 clicks)</button>
            </div>
        </div>
    `;

    setup() {
        this.clicks = useClicker();
    }

    incrementPearTree() {
        this.clicks.incrementPearTree(1);
    }

    incrementCherryTree(){
        this.clicks.incrementCherryTree(1);
    }
}