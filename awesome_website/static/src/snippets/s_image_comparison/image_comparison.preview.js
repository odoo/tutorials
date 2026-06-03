import { registry } from "@web/core/registry";
import { ImageComparison } from "./image_comparison";

const ImageComparisonEdit = (I) =>
    class extends I {
        updateSliderPosition() {
            return
        }
    };

registry
    .category("public.interactions.preview")
    .add("awesome_website.image_comparison", {
        Interaction: ImageComparison,
        mixin: ImageComparisonEdit,
    });
