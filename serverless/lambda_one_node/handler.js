var aws = require('aws-sdk');

var ec2 = new aws.EC2({apiVersion: '2016-11-15'});
var s3 = new aws.S3();
// aws.config.update({region: 'us-east-1'});


module.exports.initialise = async (event) => {
    console.log(Object.keys(event));

    if (Object.keys(event).indexOf('queryStringParameters') > -1) {
        var input = event.queryStringParameters;
        console.log('Converted input to: ', input);
    } else {
        var input = event;
        console.log('Event maintained at: ', input);
    };

    console.log('alpha')
    var s3params = {
        Bucket: 'init-whatsapp-scraper-de-serverlessdeploymentbuck-10bk8g5vdrvks', // to be read from env vars
        Key: input.user + '.json'
    };

    var ec2params = {
        InstanceIds: ['i-0cdce218490d2f160'], // to be read from env vars
        DryRun: false
    };

    console.log('bravo');
    try {
        console.log('params: ', s3params);
        const s3data = await s3.getObject(s3params).promise();
        var contacts = s3data.Body.toString('utf-8');
        var data_exists = true;
    } catch (e) {
        // data does not exist; no previous numbers found
        var data_exists = false;
    }
    if (data_exists) {
        console.log('contacts: ', contacts);
        const numbers_raw = JSON.parse(contacts.replace('\\u00d7', ''));
        console.log('numbers_raw: ', numbers_raw);
        var numbers_list = JSON.parse(numbers_raw.numbers);
        console.log('numbers_list: ', numbers_list);
    } else {
        console.log('New user detected.');
        var numbers_list = [];
    }

    try {
        const generateChips = require('./html_gen');
        var html = generateChips(input.user, numbers_list);

        console.log('engaging ec2')
        await ec2.startInstances(ec2params, function(err, data) {
            console.log('reaching out to ec2')
            if (err) {
                console.log("Error", err);
            } else if (data) {
                console.log("Success", data.StartingInstances);
            }
        }).promise();

        const response = {
            statusCode: 200,
            body: html,
            headers: {
                "Content-Type": "text/html"
            }
        };

        return response;

    } catch (e) {
        console.log('charlie')
        const response = {
            statusCode: 200,
            body: JSON.stringify(e.message),
        };
        return response;
    }
};