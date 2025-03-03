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
        this.validFrom = "2024-10-01T00:00:00";
        this.validTo   = "2099-10-01T00:00:00";
        
        this.BlokSpec =
        [
            { blokID: 1, workDay: true , from: '00 00 07 * 01-02,11-12 *', to  : '59 59 13 * 01-02,11-12 *', priceConnection: 0.912240, priceConsumption: 0.019980 }, // Višja sezona
            { blokID: 1, workDay: true , from: '00 00 16 * 01-02,11-12 *', to  : '59 59 19 * 01-02,11-12 *', priceConnection: 0.912240, priceConsumption: 0.019980 }, // Višja sezona            
                                                                
            { blokID: 2, workDay: true , from: '00 00 06 * 01-02,11-12 *', to  : '59 59 06 * 01-02,11-12 *', priceConnection: 0.912240, priceConsumption: 0.018330 }, // Višja sezona
            { blokID: 2, workDay: true , from: '00 00 14 * 01-02,11-12 *', to  : '59 59 15 * 01-02,11-12 *', priceConnection: 0.912240, priceConsumption: 0.018330 }, // Višja sezona
            { blokID: 2, workDay: true , from: '00 00 20 * 01-02,11-12 *', to  : '59 59 21 * 01-02,11-12 *', priceConnection: 0.912240, priceConsumption: 0.018330 }, // Višja sezona
            { blokID: 2, workDay: true , from: '00 00 07 * 03-10       *', to  : '59 59 13 * 03-10       *', priceConnection: 0.912240, priceConsumption: 0.018330 }, // Nižja sezona
            { blokID: 2, workDay: true , from: '00 00 16 * 03-10       *', to  : '59 59 19 * 03-10       *', priceConnection: 0.912240, priceConsumption: 0.018330 }, // Nižja sezona
            { blokID: 2, workDay: false, from: '00 00 07 * 01-02,11-12 *', to  : '59 59 13 * 01-02,11-12 *', priceConnection: 0.912240, priceConsumption: 0.018330 }, // Višja sezona
            { blokID: 2, workDay: false, from: '00 00 16 * 01-02,11-12 *', to  : '59 59 19 * 01-02,11-12 *', priceConnection: 0.912240, priceConsumption: 0.018330 }, // Višja sezona
            
            { blokID: 3, workDay: true , from: '00 00 00 * 01-02,11-12 *', to  : '59 59 05 * 01-02,11-12 *', priceConnection: 0.162970, priceConsumption: 0.018090 }, // Višja sezona
            { blokID: 3, workDay: true , from: '00 00 22 * 01-02,11-12 *', to  : '59 59 23 * 01-02,11-12 *', priceConnection: 0.162970, priceConsumption: 0.018090 }, // Višja sezona
            { blokID: 3, workDay: true , from: '00 00 06 * 03-10       *', to  : '59 59 06 * 03-10       *', priceConnection: 0.162970, priceConsumption: 0.018090 }, // Nižja sezona
            { blokID: 3, workDay: true , from: '00 00 14 * 03-10       *', to  : '59 59 15 * 03-10       *', priceConnection: 0.162970, priceConsumption: 0.018090 }, // Nižja sezona
            { blokID: 3, workDay: true , from: '00 00 20 * 03-10       *', to  : '59 59 21 * 03-10       *', priceConnection: 0.162970, priceConsumption: 0.018090 }, // Nižja sezona
            { blokID: 3, workDay: false, from: '00 00 06 * 01-02,11-12 *', to  : '59 59 06 * 01-02,11-12 *', priceConnection: 0.162970, priceConsumption: 0.018090 }, // Višja sezona
            { blokID: 3, workDay: false, from: '00 00 14 * 01-02,11-12 *', to  : '59 59 15 * 01-02,11-12 *', priceConnection: 0.162970, priceConsumption: 0.018090 }, // Višja sezona
            { blokID: 3, workDay: false, from: '00 00 20 * 01-02,11-12 *', to  : '59 59 21 * 01-02,11-12 *', priceConnection: 0.162970, priceConsumption: 0.018090 }, // Višja sezona
            { blokID: 3, workDay: false, from: '00 00 07 * 03-10       *', to  : '59 59 13 * 03-10       *', priceConnection: 0.162970, priceConsumption: 0.018090 }, // Nižja sezona
            { blokID: 3, workDay: false, from: '00 00 16 * 03-10       *', to  : '59 59 19 * 03-10       *', priceConnection: 0.162970, priceConsumption: 0.018090 }, // Nižja sezona
            
            { blokID: 4, workDay: true , from: '00 00 00 * 03-10       *', to  : '59 59 05 * 03-10       *', priceConnection: 0.004070, priceConsumption: 0.018550 }, // Nižja sezona
            { blokID: 4, workDay: true , from: '00 00 22 * 03-10       *', to  : '59 59 23 * 03-10       *', priceConnection: 0.004070, priceConsumption: 0.018550 }, // Nižja sezona
            { blokID: 4, workDay: false, from: '00 00 00 * 01-02,11-12 *', to  : '59 59 05 * 01-02,11-12 *', priceConnection: 0.004070, priceConsumption: 0.018550 }, // Višja sezona
            { blokID: 4, workDay: false, from: '00 00 22 * 01-02,11-12 *', to  : '59 59 23 * 01-02,11-12 *', priceConnection: 0.004070, priceConsumption: 0.018550 }, // Višja sezona
            { blokID: 4, workDay: false, from: '00 00 06 * 03-10       *', to  : '59 59 06 * 03-10       *', priceConnection: 0.004070, priceConsumption: 0.018550 }, // Nižja sezona
            { blokID: 4, workDay: false, from: '00 00 14 * 03-10       *', to  : '59 59 15 * 03-10       *', priceConnection: 0.004070, priceConsumption: 0.018550 }, // Nižja sezona
            { blokID: 4, workDay: false, from: '00 00 20 * 03-10       *', to  : '59 59 21 * 03-10       *', priceConnection: 0.004070, priceConsumption: 0.018550 }, // Nižja sezona
            
            { blokID: 5, workDay: false, from: '00 00 00 * 03-10       *', to  : '59 59 05 * 03-10       *', priceConnection: 0.000070, priceConsumption: 0.015550 }, // Nižja sezona
            { blokID: 5, workDay: false, from: '00 00 22 * 03-10       *', to  : '59 59 23 * 03-10       *', priceConnection: 0.000070, priceConsumption: 0.015550 }, // Nižja sezona
        ];
    }
    
    printBlokSpec()
    {
        let seasonList =
        [
            { name: "Visja", months: [ 11, 12, 1, 2 ] },
            { name: "Nizja", months: [ 3, 4, 5, 6, 7, 8, 9, 10 ] }
        ];
        
        let txt = "";
        
        txt = txt + sprintf("==========================================================================================================\n");
        
        txt = txt + sprintf("| Obdobje                |");
        
        for(let i = 1; i <= 5; i++)
        {
            txt = txt + sprintf("     CB %d      |", i);
        }
            
        txt = txt + sprintf("\n");
        
        txt = txt + sprintf("==========================================================================================================\n");
        
        
        for(let [s, season] of seasonList.entries())
        {
            for(let workDay of [ true, false ])
            {
                for(let i = 0; i < 3; i++)
                {
                    txt = txt + sprintf("|%8s|%15s|", season.name, workDay ? "delovni dan" : "dela prost dan");
                    
                    for(let b = 1; b <= 5; b++)
                    {
                        let blok = this.BlokSpec.filter(x => x.blokID === b && x.workDay === workDay && parser.parseExpression(x.from).fields.month.includes(season.months[0]));
                        
                        if(!blok || blok.length <= i) { txt = txt + sprintf("               |"); continue; }
                        
                        let from = parser.parseExpression(blok[i].from).fields.hour[0] + 0;
                        let to   = parser.parseExpression(blok[i].to  ).fields.hour[0] + 1;
                        
                        txt = txt + sprintf(" %2d:00 > %2d:00 |", from, to);
                    }
                    
                    if(i < 2) { txt = txt + sprintf("\n"); }
                }
                
                txt = txt + sprintf("\n");
                
                if(s < 1 || workDay) { txt = txt + sprintf("----------------------------------------------------------------------------------------------------------\n"); }
            }
        }
        
        txt = txt + sprintf("==========================================================================================================\n");
        
        console.log(txt);
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
     
        BlokSpec.printBlokSpec();
        
        console.log(BlokSpec.getBlok('2025-01-28T13:00:00+01:00'));
                
        // test('Blok ID2:', (t) => { assert.strictEqual(BlokSpec.getBlok('2025-01-28T14:00:00+01:00'), 2); });

    }
}

TEST();



