/** @odoo-module **/

import { patch } from "@web/core/utils/patch";
import { MapModel } from "@web_map/map_view/map_model";

patch(MapModel.prototype, {

    get canResequence() {
        if (!this.metaData.defaultOrder || this.metaData.defaultOrder.name !== "sequence") {
            this.metaData.defaultOrder = { name: "sequence", asc: true };
        }
        this.metaData.allowResequence = true;
        return (
            this.metaData.defaultOrder &&
            !this.metaData.fields[this.metaData.defaultOrder.name].readonly &&
            this.metaData.fields[this.metaData.defaultOrder.name].type === "integer" &&
            !this.metaData.groupBy?.length
        );
    },
});
