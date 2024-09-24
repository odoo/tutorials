/** @odoo-module **/

import {Component, onWillStart, useState, useEffect} from "@odoo/owl";
import {registry} from "@web/core/registry";
import {loadJS} from "@web/core/assets";
import {useService} from "@web/core/utils/hooks";
import {Layout} from "@web/search/layout";
import {DashboardItem} from "./dashboard_item";

class AwesomeDashboard extends Component {
    static template = "awesome_dashboard.AwesomeDashboard";
    static components = {Layout, DashboardItem};

    setup() {
        this.action = useService("action");
        this.statisticsService = useService("awesome_dashboard.statistics");
        this.statisticsState = useState(this.statisticsService.statistics);
        this.state = useState({
            chartJSLoaded: false,
            isChartLoading: false,
            loadChartQueue: [],
        });
        this.chart = null;

        onWillStart(() => {
            this.statisticsService.refresh()
            loadJS("/web/static/lib/Chart/Chart.js").then(() => {
                this.state.chartJSLoaded = true;
            });
        });


        useEffect(() => {
            if (
                this.statisticsState.dataAvailable &&
                !this.statisticsState.reloading &&
                this.state.chartJSLoaded &&
                this.statisticsState.orders_by_size !== undefined
            ) {
                this.enqueueLoadChart(Object.keys(this.statisticsState.orders_by_size), Object.values(this.statisticsState.orders_by_size));
            }
        }, () => [
            this.statisticsState.dataAvailable,
            this.statisticsState.reloading,
            this.statisticsState.orders_by_size,
            this.state.chartJSLoaded,
        ]);
    }

    openCustomers() {
        this.action.doAction("base.action_partner_form");
    }

    enqueueLoadChart(labels, data) {
        this.state.loadChartQueue.push({ labels, data });
        this.processQueue();
    }

    processQueue() {
        if (!this.state.isChartLoading && this.state.loadChartQueue.length > 0) {
            const nextChart = this.state.loadChartQueue.shift();
            this.loadChart(nextChart.labels, nextChart.data);
        }
    }

    async loadChart(labels, data) {
        this.state.isChartLoading = true;

        try {
            let ctx = document.getElementById('awesome_dashboard_chart').getContext('2d');
            if (this.chart) {
                this.chart.destroy();
            }
            this.chart = new Chart(ctx, {
                type: 'pie',
                data: {
                    labels: labels,
                    datasets: [{
                        label: 'Orders by size',
                        data: data,
                        borderWidth: 1
                    }]
                }
            });

        } catch (error) {
            console.error('Error loading chart:', error);
        } finally {
            this.state.isChartLoading = false;
            this.processQueue();
        }
    }

    openLeads() {
        this.action.doAction({
            type: 'ir.actions.act_window',
            name: 'Leads',
            res_model: 'crm.lead',
            views: [[false, 'list'], [false, 'form']],
        });
    }
}

registry.category("actions").add("awesome_dashboard.dashboard", AwesomeDashboard);
