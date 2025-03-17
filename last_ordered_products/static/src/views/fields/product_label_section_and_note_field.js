import { ProductLabelSectionAndNoteFieldAutocomplete } from "@account/components/product_label_section_and_note_field/product_label_section_and_note_field";
import { patch } from "@web/core/utils/patch";

patch(ProductLabelSectionAndNoteFieldAutocomplete.prototype, {
    mapRecordToOption(result) {
        let res = super.mapRecordToOption(result)
        let time_str = result[2] ? result[2] : ""
        res['time_str'] = time_str
        return res
    },
});
