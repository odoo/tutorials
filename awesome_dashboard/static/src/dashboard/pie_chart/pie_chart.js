/** @odoo-module */

import { loadJS } from "@web/core/assets";
import { getColor } from "@web/core/colors/colors";
import { Component, onWillStart, useRef, onMounted, onWillUnmount } from "@odoo/owl";
import {useService } from "@web/core/utils/hooks"

export class PieChart extends Component {
    static template = "awesome_dashboard.PieChart";
    static props = {
        label: String,
        data: Object,
    };

    setup() {
        this.canvasRef = useRef("canvas");
        onWillStart(() => loadJS(["/web/static/lib/Chart/Chart.js"]));
        onMounted(() => {
            this.renderChart();
        });
        onWillUnmount(() => {
            this.chart.destroy();
        });
        this.action = useService("action");
    }

    renderChart() {
        const labels = Object.keys(this.props.data);
        const data = Object.values(this.props.data);
        const color = labels.map((_, index) => getColor(index));
        this.chart = new Chart(this.canvasRef.el, {
            type: "pie",
            data: {
                labels: labels,
                datasets: [
                    {
                        label: this.props.label,
                        data: data,
                        backgroundColor: color,
                    },
                ],
            },
            options: {
                onClick: (event) => this.onChartClick(event),
            },
        });
    }

    onChartClick(event) {
        const activePoint = this.chart.getElementsAtEventForMode(event, "nearest", { intersect: true }, true);
        if (activePoint.length > 0) {
            const clickedLabel = this.chart.data.labels[activePoint[0].index]; 
            this.openBlankList(); 
        }
    }

    openBlankList() {
        this.action.doAction({
            type: "ir.actions.act_window",
            name: "Blank List",
            res_model: "sale.order",  
            views: [
                [false, "list"], 
                [false, "form"], 
            ],
        });
    }
}
