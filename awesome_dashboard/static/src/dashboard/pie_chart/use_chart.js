import { onWillStart, signal, useEffect } from "@odoo/owl";
import { loadJS } from "@web/core/assets";

export function useChart(getConfig) {
    const canvasRef = signal.ref();

    onWillStart(() => loadJS("/web/static/lib/Chart/Chart.js"));
    useEffect(() => {
        const canvas = canvasRef();
        if (canvasRef()) {
            const chart = new Chart(canvas, getConfig());
            return () => chart.destroy();
        }
    });
    return canvasRef;
}