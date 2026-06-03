import { registry } from "@web/core/registry";
import { ImageComparison } from "./image_comparison";

const ImageComparisonEdit = (I) =>
    class extends I {
        dynamicContent = {
            _root: {
                "t-att-class": () => ({
                    "pe-none": true,
                }),
            },
        };
        updateSliderPosition() {
            return
        }
    };

registry
    .category("public.interactions.edit")
    .add("awesome_website.image_comparison", {
        Interaction: ImageComparison,
        mixin: ImageComparisonEdit,
    });
