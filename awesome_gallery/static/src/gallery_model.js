/** @odoo-module */

import {KeepLast} from "@web/core/utils/concurrency";

export class GalleryModel {
    constructor(orm, resModel, domain, fields, archInfo) {
        this.orm = orm;
        this.resModel = resModel;
        this.domain = domain;
        this.fields = fields;
        this.archInfo = archInfo;
        this.imageField = archInfo.imageField;
        this.tooltipField = archInfo.tooltipField;
        this.images = [];
        this.keepLast = new KeepLast();
        this.pager = { offset: 0, limit: archInfo.limit };

    }

    async load() {
        const {length, records} = await this.keepLast.add(
            this.orm.webSearchRead(this.resModel, this.domain, [this.imageField, this.tooltipField], {
                limit: this.pager.limit,
                offset: this.pager.offset
            })
        );
        this.images = records;
        this.recordsLength = length;

        switch (this.fields[this.tooltipField].type) {
            case "many2one":
                this.images = records.map((record) => ({
                    ...record,
                    [this.tooltipField]: record[this.tooltipField][1],
                }));
                break;
            case "integer":
                this.images = records.map((record) => ({
                    ...record,
                    [this.tooltipField]: String(record[this.tooltipField]),
                }));
                break;
            default:
                this.images = records;
        }
    }
}
