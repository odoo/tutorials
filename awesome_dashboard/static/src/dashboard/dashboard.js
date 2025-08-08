/** @odoo-module **/

import { Component, onWillStart, onWillUnmount, useState, onWillRender } from "@odoo/owl";
import { registry } from "@web/core/registry";
import { Layout } from "@web/search/layout";
import { useService } from "@web/core/utils/hooks";
import { Card } from "./card/card";
import { PieCard } from "./pie_card/pie_card";
import { NumberCard } from "./number_card/number_card";
import { PieChart } from "./piechart/piechart";

class AwesomeDashboard extends Component {
    static template = "awesome_dashboard.AwesomeDashboard";
    static components = { Layout, Card, PieCard, NumberCard, PieChart };
    
    setup() {
        this.testData = registry.category('awesome_dashboard.data').get('graphs').map((elt) => JSON.stringify(elt));

        this.state = useState({numbers: null, graphs: null, data: null, happygary: 'ᕦ( ᐛ )ᕡ'});
        
        this.onStatsUpdate = (vals) => {
            this.state.data = vals;
        }
        
        this.dance = () => {
            this.state.happygary = this.state.happygary == 'ᕦ( ᐛ )ᕡ' ? 'ᕕ( ᐕ )ᕗ' : 'ᕦ( ᐛ )ᕡ'
            setTimeout(() => {this.dance();}, 700)
        }

        this.dance();
        
        this.action = useService('action');
        
        this.statsService = useService('awesome_dashboard.stats');


        onWillStart(async () => {
            this.statsService.setActive(this.onStatsUpdate);
            this.state.data = await this.statsService.getValues();
        });

        onWillUnmount(() => {this.statsService.clearActive()});

        onWillRender(() => {
            const numbers = registry.category('awesome_dashboard.data').get('numbers');
            const directValues = numbers.filter((elt) => elt.source == null);
            const loadedValues = numbers.filter((elt) => elt.source).map((elt) => {
                elt.value = this.state.data[elt.source];
                return elt;
            });

            this.state.numbers = [
                ...loadedValues,
                ...directValues,
            ].map((elt) => JSON.stringify(elt));

            const graphs = registry.category('awesome_dashboard.data').get('graphs');
            const directCharts = graphs.filter((elt) => elt.source == null);
            const loadedCharts = graphs.filter((elt) => elt.source).map((elt) => {
                elt.data = this.state.data[elt.source];
                return elt;
            });

            this.state.graphs = [
                ...loadedCharts,
                ...directCharts,
            ].map((elt) => JSON.stringify(elt));
        });

    }
    
    customersButton() {
        this.action.doAction('base.action_partner_form');
    }

    leadsButton() {
        this.action.doAction({
            type: 'ir.actions.act_window',
            name: 'Leads',
            target: 'current',
            res_model: 'crm.lead',
            views: [[false, 'list'], [false, 'form']],
        });
    }

}

registry.category("lazy_components").add("awesome_dashboard.dashboard", AwesomeDashboard);
