let axios = require("axios");
let Moment = require('moment');
var sprintf = require('sprintf-js').sprintf;

class connectorWorkFreeDays
{
    constructor()
    {
        this.freeDays = [];
    }
    
    async setPublicHolidays(year, iso2)
    {
        let publicHolidays = this.freeDays.find(x => x.iso2);
        
        if(!publicHolidays)
        {
            publicHolidays = { iso2: iso2, dates: [] };
            
            this.freeDays.push(publicHolidays);
        }
        
        let config =
        {
            method: 'get',
            url: sprintf("%s/%d/%s", "https://date.nager.at/api/v3/PublicHolidays", year, iso2)
        };
       
        return await axios.request(config).then((response) =>
        {
            publicHolidays.dates =
            [
                ...publicHolidays.dates,
                ...response.data.filter(x => x.types.includes("Public")).map(x => { return { date: Moment(x.date), name: x.name }; })
            ];
        })
        .catch((error) =>
        {
            console.log(error);
            
            throw new Error("setPublicHolidays");
        });
    }
    
    async isWorkFreeDay(date)
    {
        if(Moment(date).day() === 6) { return true; } // Saturday
        if(Moment(date).day() === 7) { return true; } // Sunday
        
        if(this.freeDays.includes(Moment(date)))
        {
            return true;
        }
        
        return false;
    }
}

async function INIT()
{
    let API = new connectorWorkFreeDays();
        
    await API.setPublicHolidays(2020, 'SI');
    await API.setPublicHolidays(2021, 'SI');
    await API.setPublicHolidays(2022, 'SI');
    await API.setPublicHolidays(2023, 'SI');
    await API.setPublicHolidays(2024, 'SI');
    await API.setPublicHolidays(2025, 'SI');
    
    return API;
}

async function TEST()
{
    if(require.main === module)
    {
        console.log("Connector [TEST]: WorkFreeDays");
        
        let API = await INIT();
        
        console.log(API.isWorkFreeDay("2025-02-01"));
    }
}

TEST();

module.exports = INIT;
