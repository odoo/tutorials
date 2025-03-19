import { registry } from '@web/core/registry';

export const clickerCommands = [
    {
        name: 'Open clicker game',
        services: ['action'],
        action: services => {
            services[0].doAction({
                type: 'ir.actions.client',
                tag: 'awesome_clicker.client_action',
                target: 'new',
                name: 'Clicker' 
            });
        }
    },
    {
        name: 'Buy a clickbot',
        services: ['awesome_clicker.clicker', 'notification'],
        action: services => {
            if (!services[0].clickBot.buy(services[0])) {
                services[1].add("You do not have the resources needed to buy a clickbot", {
                    type: 'danger'
                });
            }
        }
    },
    {
        name: 'Buy a bigbot',
        services: ['awesome_clicker.clicker', 'notification'],
        action: services => {
            if (!services[0].bigBot.buy(services[0])) {
                services[1].add("You do not have the resources needed to buy a bigbot", {
                    type: 'danger'
                });
            }
        }
    }
];

const commandProviderRegistry = registry.category("command_provider");
commandProviderRegistry.add('awesome_clicker', {
    provide: (env, options) => {
        const result = [];
        for (const command of clickerCommands) {
            const services = [];
            for (const serviceName of command.services) {
                services.push(env.services[serviceName]);
            }
            result.push({
                name: command.name,
                category: 'awesome_clicker',
                action: () => command.action(services),
            });
        }
        return result;
    }
});
