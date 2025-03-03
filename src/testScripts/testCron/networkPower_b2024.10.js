var parser = require('cron-parser');
const test = require('node:test');
var assert = require('assert');
var sprintf = require('sprintf-js').sprintf;

const Moment = require('moment');
const MomentRange = require('moment-range');
 
const moment = MomentRange.extendMoment(Moment);

class ParseBlok
{
    constructor()
    {
        this.validFrom = "2020-01-01T00:00:00";
        this.validTo   = "2024-10-01T00:00:00";
        
        this.powerConnection = 0.796000; // price per kW
        
        this.BlokSpec =
        [
            { "defId": 1, "workDay": true , "from": "00 00 00 * * *", "to": "59 59 05 * * *", "priceConsumption": 0.033110 }, // Mala Tarifa
            { "defId": 1, "workDay": true , "from": "00 00 22 * * *", "to": "59 59 23 * * *", "priceConsumption": 0.033110 }, // Mala Tarifa
            { "defId": 1, "workDay": false, "from": "00 00 00 * * *", "to": "59 59 23 * * *", "priceConsumption": 0.033110 }, // Mala Tarifa
            
            { "defId": 2, "workDay": true , "from": "00 00 06 * * *", "to": "59 59 21 * * *", "priceConsumption": 0.043080 } // Visoka Tarifa
        ];
    }
    
    getBlok(date)
    {
        for(let BlokTime of this.BlokSpec)
        {
            let parseFrom = parser.parseExpression(BlokTime.from, { currentDate: moment(date).add(1, "seconds").toISOString() });
            let parseTo   = parser.parseExpression(BlokTime.to,   { currentDate: moment(date).add(1, "seconds").toISOString() });
            
            const range = moment.range(parseFrom.prev().toISOString(), parseTo.next().toISOString());
            
            if(range.diff('days') === 0 && range.contains(moment(date)))
            {
                return BlokTime;
            }
        }
        
        return null;
    }
    
}

async function TEST()
{
    if(require.main === module)
    {
        let BlokSpec = new ParseBlok();
     
        console.log(BlokSpec.getBlok('2023-01-28T13:00:00+01:00'));

    }
}

TEST();



