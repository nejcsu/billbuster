var parser = require('cron-parser');
const test = require('node:test');
var assert = require('assert');
const Moment = require('moment');
const MomentRange = require('moment-range');
 
const moment = MomentRange.extendMoment(Moment);

class ParseBlok
{
    constructor()
    {
        this.BlokSpec =
        [
            { blokID: 2, workDay: true, from: '00 00 07 * 03-10 *', to  : '59 59 13 * 03-10 *' }, // Nižja sezona
            { blokID: 2, workDay: true, from: '00 00 16 * 03-10 *', to  : '59 59 19 * 03-10 *' }, // Nižja sezona
            { blokID: 2, workDay: true, from: '00 00 06 * 11-12 *', to  : '59 59 06 * 11-12 *' }, // Višja sezona
            { blokID: 2, workDay: true, from: '00 00 14 * 11-12 *', to  : '59 59 15 * 11-12 *' }, // Višja sezona
            { blokID: 2, workDay: true, from: '00 00 20 * 11-12 *', to  : '59 59 21 * 11-12 *' }, // Višja sezona
            { blokID: 2, workDay: true, from: '00 00 06 * 01-02 *', to  : '59 59 06 * 01-02 *' }, // Višja sezona
            { blokID: 2, workDay: true, from: '00 00 14 * 01-02 *', to  : '59 59 15 * 01-02 *' }, // Višja sezona
            { blokID: 2, workDay: true, from: '00 00 20 * 01-02 *', to  : '59 59 21 * 01-02 *' }, // Višja sezona
        ];
    }
    
    getBlokID(date)
    {
        for(let BlokTime of this.BlokSpec)
        {
            // console.log(BlokTime);
            
            let parseFrom = parser.parseExpression(BlokTime.from, { currentDate: moment(date).add(1, "seconds").toISOString() });
            let parseTo   = parser.parseExpression(BlokTime.to,   { currentDate: moment(date).add(1, "seconds").toISOString() });
            
            // console.log(parseFrom.prev());
            // console.log(parseTo.next());
            
            const range = moment.range(parseFrom.prev().toISOString(), parseTo.next().toISOString());
            
            // console.log(range);
            
            if(range.diff('days') === 0 && range.contains(moment(date)))
            {
                // console.log(range);
                return BlokTime.blokID;
            }
            
            // console.log(moment(date));
            // console.log(range);
            // console.log(range.diff('days'));
            // console.log(range.contains(moment(date)));
        }
        
        return null;
    }
    
}

async function TEST()
{
    if(require.main === module)
    {
        let BlokSpec = new ParseBlok();
        
        console.log(BlokSpec.getBlokID('2025-01-28T14:00:00+01:00'));
        
        // const cron = parser.parseExpression('0 0 7  * 03-10 *', { currentDate: '2025-01-28 00:00:01' });
        // 
        // console.log(cron.next().toString())
        // console.log(cron.next().toString())
        // console.log(cron.next().toString())
        // console.log(cron.next().toString())
        // console.log(cron.next().toString())
        // console.log(cron.next().toString())
        // console.log(cron.next().toString())
        
        test('Blok ID2:', (t) => { assert.strictEqual(BlokSpec.getBlokID('2025-01-28T14:00:00+01:00'), 2); });

        
    }
}

TEST();



