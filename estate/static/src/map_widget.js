/** @odoo-module */
import { registry } from "@web/core/registry";
import { Component } from "@odoo/owl";
import { standardFieldProps } from "@web/views/fields/standard_field_props";
import { loadJS } from "@web/core/assets";
import { useService } from "@web/core/utils/hooks";


export class MapField extends Component {
    static template = "estate.MapField";

    setup() {
        this.notification = useService("notification");
        loadJS("https://unpkg.com/leaflet@1.9.4/dist/leaflet.js").then(() => {
            this.waitForMapElement()
                .then(() => {
                    const coordinates = this.value !== null ? [this.value[0][0], this.value[0][1]] : null;
                    this.initializeMap(coordinates);
                })
                .catch((error) => {
                    // use odoo's error handling
                    this.notification.add(error, { type: "danger" });
                });
        });
    }

    async waitForMapElement(timeout = 1000) {
        const pollInterval = 100;
        const start = performance.now();
        return new Promise((resolve, reject) => {
            const checkMapExists = () => {
                console.log("Waiting for map element...");
                if (document.getElementById("map")) {
                    resolve();
                } else if (performance.now() - start > timeout) {
                    reject("Map element not found");
                } else {
                    setTimeout(checkMapExists, pollInterval);
                }
            };
            checkMapExists();
        });
    }

    initializeMap(coordinates) {
        // If no coordinates exist, set a default view over a general location (e.g., the whole world)
        const defaultCoordinates = coordinates || [20.0, 0.0];
        const defaultZoom = coordinates ? 10 : 2;

        const map = L.map('map').setView(defaultCoordinates, defaultZoom);

        L.tileLayer('https://tile.openstreetmap.org/{z}/{x}/{y}.png', {
            maxZoom: 18,
            minZoom: 2
        }).addTo(map);

        let marker = coordinates ? L.marker(coordinates).addTo(map) : null;
        this.addMapClickListener(map, marker);
    }

    addMapClickListener(map, marker) {
        map.on('click', (e) => {
            const { lat, lng } = e.latlng;
            if (!marker) {
                marker = L.marker([lat, lng]).addTo(map);
            } else {
                marker.setLatLng([lat, lng]);
            }
            this.updateRecord(lat, lng);
            const zoomLevel = map.getZoom() < 10 ? 10 : map.getZoom();
            map.setView([lat, lng], zoomLevel);
        });
    }

    updateRecord(lat, lng) {
        this.props.record.update({
            [this.props.name]: `${lat},${lng}`
        });
    }

    get value() {
        return this.props.record.data[this.props.name];
    }
}

MapField.props = {
    ...standardFieldProps,
};
MapField.supportedTypes = ["geo_point"];

export const mapField = {
    component: MapField,
    displayName: "MapField",
    supportedOptions: [],
    supportedTypes: ["string"],
    isEmpty: () => false,
};

registry.category("fields").add("map_widget", mapField);
