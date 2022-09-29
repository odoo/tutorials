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
    }

    async load(domain) {
        const { records } = await this.keepLast.add(
            this.orm.webSearchRead(this.resModel, domain, {
                limit: this.limit,
                specification: {
                    [this.imageField]: {},
                    ...( this.tooltipField ? {[this.tooltipField]: {}}: {}),
                },
                context: {
                    bin_size: true,
                }
            })
        );

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
}
