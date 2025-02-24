import { Component, useRef, onMounted } from "@odoo/owl";
import { useService } from "@web/core/utils/hooks";
import { loadJS } from "@web/core/assets";

export class PieChart extends Component {
    static template = "awesome_dashboard.PieChart";  
    canvasRef = useRef("chartCanvas");  
    setup() {
        this.statsService = useService("awesome_dashboard.statistics");
        this.sizeData = this.statsService.statistics.sizedata;
        onMounted(async () => {
            await loadJS("/web/static/lib/Chart/Chart.js");
            if (Object.keys(this.sizeData).length > 0) {
                this.renderChart();
            }
        });
    }
    renderChart() {
        if (!this.canvasRef.el) {
            console.error("Canvas element is not ready.");
            return;
        }
        const ctx = this.canvasRef.el.getContext("2d");
        new Chart(ctx, {
            type: "pie",
            data: {
                labels: Object.keys(this.sizeData),
                datasets: [{
                    data: Object.values(this.sizeData),
                    backgroundColor: ["red", "blue", "green", "yellow", "purple"], 
                }]
            },
        });
    }
}
