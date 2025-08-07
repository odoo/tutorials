"use strict";
import { Component, onWillStart, useRef, useEffect } from '@odoo/owl'
import { AssetsLoadingError, loadJS } from '@web/core/assets';

export class PieChartCard extends Component {

    static template = "awesome_dashboard.pieChartCard";
    static components = {}
    static props = {
        title: {
            type: String
        },
        value: {
            type: Object
        }
    }

    setup() {
        this.canvasRef = useRef("canvas");

        onWillStart(async () => {
            try {
                await loadJS(["/web/static/lib/Chart/Chart.js"]);
            } 
            catch (error) {
                if (!(error instanceof AssetsLoadingError)) {
                    throw error;
                }
            }
        })

        useEffect(() => this.renderPieChart())
    }

    renderPieChart() {
        const ctx = this.canvasRef.el.getContext("2d");
        if (this.chart) {
            this.chart.destroy();
        }
        this.chart = new Chart(ctx, {   
            type: "pie",
            data: {
                labels: Object.keys(this.props.value || []), //["S", "M", "L", "XL", "XXL"],
                datasets: [{
                    data: Object.values(this.props.value || []), // [10, 20, 15, 5, 2]
                }],
            },
            options: {
                responsive: true,
            },
        });
    }
}
