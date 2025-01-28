let Moment = require('moment');
let MomentRange = require('moment-range');
let fs = require("fs");
let axios = require("axios");
let sprintf = require('sprintf-js').sprintf;

const moment = MomentRange.extendMoment(Moment);

class MojElektro
{
    // Swagger: https://docs.informatika.si/mojelektro/api
    //
    // Topologija:
    // MerilnoMesto > 1..* > MerilnaTocka
    // MerilnoMesto > 1..* > MeterReadings
    
    constructor(akey, mmid)
    {
        this.mmid = mmid;
        this.akey = akey;
        
        this.host = "https://api.informatika.si/mojelektro/v1/";
    }

    async getMerilnoMesto()
    {
        let config =
        {
            method: 'get',
            url: sprintf("%s/merilno-mesto/%s", this.host, this.mmid),
            headers: { 'x-api-token': this.akey }
        };
        
        return await axios.request(config).then((response) =>
        {
            return response.data;
        })
        .catch((error) =>
        {
            console.log(error);
            
            throw new Error("getMerilnoMesto");
        });
    }
    
    async getMerilnaTocka(gsrn)
    {
        let config =
        {
            method: 'get',
            url: sprintf("%s/merilna-tocka/%s", this.host, gsrn),
            headers: { 'x-api-token': this.akey }
        };
       
        return await axios.request(config).then((response) =>
        {
            return response.data;
        })
        .catch((error) =>
        {
            console.log(error);
            
            throw new Error("getMerilnaTocka");
        });
    }
    
    async getMeterReadings(from, to)
    {
        var params = new URLSearchParams();
        
        params.append("usagePoint", this.mmid);
        
        params.append("startTime", from);
        params.append("endTime"  , to  );
        
        params.append("option"  , "ReadingType=32.0.2.4.1.2.12.0.0.0.0.0.0.0.0.3.72.0" ); // Prejeta 15 minutna delovna energija
        params.append("option"  , "ReadingType=32.0.2.4.19.2.12.0.0.0.0.0.0.0.0.3.72.0"); // Oddana 15 minutna delovna energija
        params.append("option"  , "ReadingType=32.0.2.4.1.2.12.0.0.0.0.0.0.0.0.3.73.0" ); // Prejeta 15 minutna jalova energija
        params.append("option"  , "ReadingType=32.0.2.4.19.2.12.0.0.0.0.0.0.0.0.3.73.0"); // Oddana 15 minutna jalova energija
        params.append("option"  , "ReadingType=32.0.2.4.1.2.37.0.0.0.0.0.0.0.0.3.38.0" ); // Prejeta 15 minutna delovna moč
        params.append("option"  , "ReadingType=32.0.2.4.19.2.37.0.0.0.0.0.0.0.0.3.38.0"); // Oddana 15 minutna delovna moč
        params.append("option"  , "ReadingType=32.0.2.4.1.2.37.0.0.0.0.0.0.0.0.3.63.0" ); // Prejeta 15 minutna jalova moč
        params.append("option"  , "ReadingType=32.0.2.4.19.2.37.0.0.0.0.0.0.0.0.3.63.0"); // Oddana 15 minutna jalova moč
        params.append("option"  , "ReadingType=32.0.4.1.1.2.12.0.0.0.0.0.0.0.0.3.72.0" ); // Prejeta delovna energija ET
        params.append("option"  , "ReadingType=32.0.4.1.1.2.12.0.0.0.0.1.0.0.0.3.72.0" ); // Prejeta delovna energija VT
        params.append("option"  , "ReadingType=32.0.4.1.1.2.12.0.0.0.0.2.0.0.0.3.72.0" ); // Prejeta delovna energija MT
        params.append("option"  , "ReadingType=32.0.4.1.19.2.12.0.0.0.0.0.0.0.0.3.72.0"); // Oddana delovna energija ET
        params.append("option"  , "ReadingType=32.0.4.1.19.2.12.0.0.0.0.1.0.0.0.3.72.0"); // Oddana delovna energija VT
        params.append("option"  , "ReadingType=32.0.4.1.19.2.12.0.0.0.0.2.0.0.0.3.72.0"); // Oddana delovna energija MT
        params.append("option"  , "ReadingType=32.0.4.1.1.2.12.0.0.0.0.0.0.0.0.3.73.0" ); // Prejeta jalova energija ET
        params.append("option"  , "ReadingType=32.0.4.1.1.2.12.0.0.0.0.1.0.0.0.3.73.0" ); // Prejeta jalova energija VT
        params.append("option"  , "ReadingType=32.0.4.1.1.2.12.0.0.0.0.2.0.0.0.3.73.0" ); // Prejeta jalova energija MT
        params.append("option"  , "ReadingType=32.0.4.1.19.2.12.0.0.0.0.0.0.0.0.3.73.0"); // Oddana jalova energija ET
        params.append("option"  , "ReadingType=32.0.4.1.19.2.12.0.0.0.0.1.0.0.0.3.73.0"); // Oddana jalova energija VT
        params.append("option"  , "ReadingType=32.0.4.1.19.2.12.0.0.0.0.2.0.0.0.3.73.0"); // Oddana jalova energija MT
        
        let config =
        {
            method: 'get',
            url: sprintf("%s/meter-readings", this.host),
            headers:
            {
                'x-api-token': this.akey
            },
            params: params
        };
       
        return await axios.request(config).then((response) =>
        {
            return response.data;
        })
        .catch((error) =>
        {
            console.log(error);
            
            throw new Error("getMeterReadings");
        });
    }
    
    async SaveToFile()
    {
        let rawData = { ver: "1.0.0.0", key: this.akey, mid: this.mmid, meterReadings: [] };
        
        rawData.merilnoMesto = await this.getMerilnoMesto();
        
        for(let merilnaTocka of rawData.merilnoMesto.merilneTocke)
        {
            merilnaTocka.podatki = await this.getMerilnaTocka(merilnaTocka.gsrn);
        }
        
        const start = moment().add(-2, 'years');
        const end   = moment().add(-2, 'days' );
        
        const range = moment.range(start, end);
        
        for (let day of range.by('day', { step: 30 }))
        {
            let from = day.add(0 , "days").format('YYYY-MM-DD');
            let to   = day.add(30, "days").format('YYYY-MM-DD');
            
            rawData.meterReadings.push(await this.getMeterReadings(from, to));
        }
        
        fs.writeFileSync(sprintf("%s - %s.json", moment().format('YYYY-MM-DD'), this.mmid), JSON.stringify(rawData));
    }
}

async function TEST()
{
    if(require.main === module)
    {
        console.log("Connector [TEST]: MojElektro");
        
        let merilnoMestoID = "#-######";
        
        let ApiKey = "#######";
        
        let API = new MojElektro(ApiKey, merilnoMestoID);
        
        // console.log(await API.getMerilnoMesto());
        // 
        // console.log(await API.getMeterReadings("2024-12-28", "2024-12-30"));
        
        await API.SaveToFile();
    }
}

TEST();

module.exports = MojElektro;
