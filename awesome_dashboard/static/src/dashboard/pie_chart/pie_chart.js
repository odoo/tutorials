import { loadJS } from "@web/core/assets";
import { useService } from "@web/core/utils/hooks";
import { Component, onWillStart, onWillUnmount, useEffect, useRef } from "@odoo/owl";
    
export class PieChart extends Component {
    static template = "awesome_dashboard.pie_chart";
    static props = {
        title: String,
        data: Object,
    };

    setup() {        
        this.canvasRef = useRef("canvas")
        this.action = useService("action");

        onWillStart(async () => {
            await loadJS("/web/static/lib/Chart/Chart.js");
        });

        useEffect(() => {
            if (this.pieChart) {
                this.pieChart.destroy();
            }
            this.renderPieChart();
        });
        onWillUnmount(() => {
            if (this.pieChart) {
                this.pieChart.destroy();
            }
        });
    }

    renderPieChart() {
        if (!this.canvasRef.el || !this.props.data) {
            return;
        }
        const key = Object.keys(this.props.data);
        const value = Object.values(this.props.data);
        const backgroundColor = [
            'rgba(255, 99, 132, 0.2)',
            'rgba(54, 162, 235, 0.2)',
            'rgba(255, 206, 86, 0.2)',
            'rgba(75, 192, 192, 0.2)',
            'rgba(153, 102, 255, 0.2)',
            'rgba(255, 159, 64, 0.2)'
        ];
        const borderColor = [
            'rgba(255, 99, 132, 1)',
            'rgba(54, 162, 235, 1)',
            'rgba(255, 206, 86, 1)',
            'rgba(75, 192, 192, 1)',
            'rgba(153, 102, 255, 1)',
            'rgba(255, 159, 64, 1)'
        ];

        this.pieChart = new Chart(this.canvasRef.el, {
            type: 'pie',
            data: {
                labels: key,
                datasets: [{
                    label: this.props.title,
                    data: value,
                    backgroundColor: backgroundColor,
                    borderColor: borderColor,
                    borderWidth: 1
                }]
            },
            options: {
                onClick: (event, elements) => {
                    if(elements.length > 0){
                        const index = elements[0].index;
                        const size = Object.keys(this.props.data)[index];
                        this.action.doAction({
                            type: "ir.actions.act_window",
                            name: "Orders List",
                            res_model: "sale.order",
                            views: [
                                [false, 'list'],
                                [false, 'form']],
                            domain: [
                                ['order_line.name', 'ilike', size]
                            ],
                        });
                    }
                }
            }
        });
    }
}
