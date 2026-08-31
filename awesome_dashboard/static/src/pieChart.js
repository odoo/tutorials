import { Component, onWillStart, useRef, useEffect } from "@odoo/owl";
import { loadJS } from "@web/core/assets";


export class PieChart extends Component {
    static template = "awesome_dashboard.PieChart";
 
    setup() {
        onWillStart(() => loadJS("/web/static/lib/Chart/Chart.js"));
        this.canvasRef = useRef("canvas");
        const data ={
            "m": 79,
            "s": 90,
            "xl": 49
        }
        useEffect(() => {
            
            this.chart = new Chart(
                this.canvasRef.el,
                {
                    type: 'pie',
                    data: {
                        labels: Object.keys(data),
                        datasets: [{
                            data: Object.values(data)
                        }]
                    },
                    size: {
                        width: 1000,
                        height: 1000
                    }
                }
            )
        });
    }

}
