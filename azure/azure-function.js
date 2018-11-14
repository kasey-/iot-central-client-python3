const sgMail = require('@sendgrid/mail');
const Cache = require('ttl');

const sendgrid_key = 'ADD HERE SENDGRID KEY';
const email_from = 'ADD HERE FROM EMAIL';
const email_to = 'ADD HERE DEST EMAIL';
const ttl_life = 60; // seconds

sgMail.setApiKey(sendgrid_key);
let cache = new Cache({
    ttl: ttl_life * 1000,
    capacity: 100
});

module.exports = async function (context, req) {
    const timestamp = req.body.timestamp;
    const rule = req.body.rule;
    const device = req.body.device;
    const app = req.body.application;
    const measure = req.body.device.measurements;

    const app_name = app.name;
    const rule_name = rule.name;
    const device_name = device.name;
    const measure_telemetry = measure.telemetry;

    const device_session = cache.get(device_name);
    cache.put(device_name,measure_telemetry);

    if(device_session === undefined) {
        const msg = `${timestamp} - ${app_name} - ${rule_name} - ${device_name} - ${JSON.stringify(measure_telemetry)}`;
        const mail = {
            to: email_to,
            from: email_from,
            subject: `Alert: ${rule_name} ${device_name}`,
            text: msg,
            html: `<p>${msg}</p>`
        };
        sgMail.send(mail);
    }

    context.res = {
        status: 200,
        body: ""
    };
};
