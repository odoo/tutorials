/** @odoo-module */

import {KeepLast} from "@web/core/utils/concurrency";

export class GalleryModel {
    constructor(orm, resModel, archInfo, fields) {
        this.orm = orm;
        this.resModel = resModel;
        this.imageField = archInfo.imageField;
        this.limit = archInfo.limit;
        this.tooltipField = archInfo.tooltipField;
        this.fields = fields;
        this.keeplast = new KeepLast();
    }

    async loadImages(domain) {
        const { records } = await this.keeplast.add(
            this.orm.webSearchRead(this.resModel, domain, {
                limit: this.limit,
                specification: {
                    [this.imageField]: {},
                    ...(this.tooltipField ? {[this.tooltipField] : {}} : {}),
                },
                context: {
                    bin_size: true,
                }
            })
        );

        if(!this.tooltipField) {
            this.records = records;
            return;
        }

        switch(this.fields[this.tooltipField].type) {
            case "many2one":
                this.records = records.map((record) => ({
                    ...record,
                    [this.tooltipField]: record[this.tooltipField][1],
                }));
                break;
            case "integer":
                this.records = records.map((record) => ({
                    ...record,
                    [this.tooltipField]: String(record[this.tooltipField]),
                }));
                break;
            default:
                this.records = records;
        }
    }
}
