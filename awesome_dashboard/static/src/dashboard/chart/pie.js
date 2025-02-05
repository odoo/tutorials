import { Component, useRef, onWillStart, useEffect } from "@odoo/owl";
import { loadJS } from "@web/core/assets";

export class PieChart extends Component {
    static template = "awesome_dashboard.pie_chart";
    static props = {
        data: { type: Object },
    };

    setup() {
        this.canvasRef = useRef('canvasRef');
        this.chart = null;

        onWillStart(async () => {
            await loadJS(["/web/static/lib/Chart/Chart.js"]);
        });

        useEffect(()=> this.renderChart())

    }

    renderChart() {
      if (this.chart) {
          this.chart.destroy();}
      this.chart = new Chart(this.canvasRef.el, this.getChartConfig());
    }

    getChartConfig() {
        return {
            type: 'pie',
            data: {
                labels: this.props.labels,
                datasets: [{
                    data: Object.values(this.props.data)    
                }],
            },
        }
    }

}
