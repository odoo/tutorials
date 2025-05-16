import { DashboardSettings } from "./dashboard_settings";

export function useSettingsDialog(dialogService) {
    return new Promise((resolve) => {
      dialogService.add(
        DashboardSettings,
        {
          confirm: resolve,
        },
        {
          close: () => resolve(false),
        }
      );
    });
}
