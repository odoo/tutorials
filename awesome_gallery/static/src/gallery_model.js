/** @odoo-module */

import { KeepLast } from "@web/core/utils/concurrency";

export class GalleryModel {
    constructor(orm, resModel, fields, archInfo) {
        this.orm = orm;
        this.resModel = resModel;
        const { imageField, limit, fieldsForTooltip } = archInfo;
        this.fieldsForTooltip = fieldsForTooltip;
        this.imageField = imageField;
        this.fields = fields;
        this.limit = limit;
        this.keepLast = new KeepLast();
        this.pager = { offset: 0, limit: limit };
    }

    async load(domain) {
        const specification = {
            [this.imageField]: {},
            write_date: {},
        }
        for (const field of this.fieldsForTooltip) {
            specification[field] = {};
        }
        const { length, records } = await this.keepLast.add(
            this.orm.webSearchRead(this.resModel, domain, {
                limit: this.pager.limit,
                offset: this.pager.offset,
                specification,
                context: {
                    bin_size: true,
                }
            })
        );
        this.recordsLength = length;
        this.records = records;
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
