import { BuilderAction } from "@html_builder/core/builder_action";
import { Plugin } from "@html_editor/plugin";
import { registry } from "@web/core/registry";

class ImageComparisonOptionPlugin extends Plugin {
    static id = "awesome_website.ImageComparison";

    resources = {
        builder_actions: { SetCompareSliderDirectionAction },
    };
}

class SetCompareSliderDirectionAction extends BuilderAction {
    static id = "setCompareSliderDirection";

    isApplied({ editingElement, params: { mainParam: param } }) {
        return editingElement.classList.contains(`o_image_comparison_${param}`);
    }
    apply({ editingElement, params: { mainParam: param } }) {
        editingElement.classList.add(`o_image_comparison_${param}`);
    }
    clean({ editingElement, params: { mainParam: param } }) {
        editingElement.classList.remove(`o_image_comparison_${param}`);
    }
}

registry.category("website-plugins").add(ImageComparisonOptionPlugin.id, ImageComparisonOptionPlugin);
