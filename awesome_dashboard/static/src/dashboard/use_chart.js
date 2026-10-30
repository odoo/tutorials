import { onWillStart, signal, useEffect } from "@odoo/owl";
import { loadJS } from "@web/core/assets";

export function useChart(descFn) {
    const canvasRef = signal.ref();
    let chart = null;

    onWillStart(() => loadJS("/web/static/lib/Chart/Chart.js"));

    useEffect(() => {
        const canvas = canvasRef();
        if (canvas) {
            chart = new Chart(canvas, descFn());
            return () => chart.destroy();
        }
    });

    return canvasRef;
}