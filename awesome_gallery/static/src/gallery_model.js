/** @odoo-module */

import { KeepLast } from "@web/core/utils/concurrency";

export class GalleryModel {
    constructor(orm, resModel, fields, archInfo) {
        this.orm = orm;
        this.resModel = resModel;
        const { imageField, limit, tooltipField } = archInfo;
        this.imageField = imageField;
        this.fields = fields;
        this.limit = limit;
        this.tooltipField = tooltipField;
        this.keepLast = new KeepLast();
        this.pager = { offset: 0, limit: limit };
    }

    async load(domain) {
        const { length, records } = await this.keepLast.add(
            this.orm.webSearchRead(this.resModel, domain, {
                limit: this.pager.limit,
                offset: this.pager.offset,
                specification: {
                    [this.imageField]: {},
                    ...( this.tooltipField ? {[this.tooltipField]: {}}: {}),
                    write_date: {}
                },
                context: {
                    bin_size: true,
                }
            })
        );
        this.recordsLength = length;

        if (!this.tooltipField) {
            this.records = records;
            return;
        }

        switch (this.fields[this.tooltipField].type) {
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

    async uploadImage(record_id, image_binary, domain) {
        await this.orm.webSave(
            this.resModel,
            [record_id],
            {
                [this.imageField]: image_binary,
            },
            {
                specification: {},
            }
        )
        await this.load(domain);
    }
}
