const sgMail = require('@sendgrid/mail');
const Cache = require('ttl');

const sendgrid_key = process.env['SENDGRID_KEY'];
const email_from = process.env['EMAIL_FROM'];
const email_to = process.env['EMAIL_TO'];
const ttl_life = parseInt(process.env['TTL_LIFE']); // seconds

sgMail.setApiKey(sendgrid_key);
let cache = new Cache({
    ttl: ttl_life * 1000,
    capacity: 100
});

module.exports = async function (context, req) {
    const {
        timestamp,
        application:{name:app_name},
        rule:{name:rule_name},
        device:{
            name:device_name,
            measurements:{telemetry:measure_telemetry}
        }
    } = req.body;

    const device_session = cache.get(device_name);

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
        cache.put(device_name,measure_telemetry);
    }

    context.res = {
        status: 200,
        body: ""
    };
};
