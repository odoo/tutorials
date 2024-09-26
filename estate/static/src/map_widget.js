/** @odoo-module */
import { registry } from "@web/core/registry";
import { Component, useState } from "@odoo/owl";
import { standardFieldProps } from "@web/views/fields/standard_field_props";
import { loadJS } from "@web/core/assets";
import { parseFloat } from "@web/views/fields/parsers";


export class MapField extends Component {
    static template = "estate.MapField";

    // when ready and rendered
    setup() {
        loadJS("https://unpkg.com/leaflet@1.9.4/dist/leaflet.js").then((e) => {


            var map = L.map('map').setView([this.value[0][0], this.value[0][1]], 13);

            L.tileLayer('https://tile.openstreetmap.org/{z}/{x}/{y}.png').addTo(map);

            let marker = L.marker([this.value[0][0], this.value[0][1]]).addTo(map);

            // write coordinates to input field when map is clicked

            map.on('click', (e) => {
                var lat = e.latlng.lat;
                var lon = e.latlng.lng;

                marker.setLatLng([lat, lon]);
                // console.log(this.props.record.update)
                this.props.record.update({[this.props.name]: `${lat},${lon}`});
            });
        });
    }


    // get coordinates() {
    //     console.log(this.update)
    //     return this.props.record.data[this.props.name][0];
    // }

    // onFocusIn() {
        // this.state.hasFocus = true;
    // }

    // onFocusOut() {
        // this.state.hasFocus = false;
    // }

    // parse(value) {
        // return this.props.inputType === "number" ? Number(value) : parseFloat(value);
    // }

    // get formattedValue() {
        // if (
        //     !this.props.formatNumber ||
        //     (this.props.inputType === "number" && !this.props.readonly && this.value)
        // ) {
        //     return this.value;
        // }
        // if (this.props.humanReadable && !this.state.hasFocus) {
        //     return formatFloat(this.value, {
        //         digits: this.digits,
        //         humanReadable: true,
        //         decimals: this.props.decimals,
        //     });
        // } else {
        //     return formatFloat(this.value, { digits: this.digits, humanReadable: false });
        // }
    // }

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
