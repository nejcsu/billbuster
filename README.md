# billbuster
Check your options and reduce your electricity bill

EU countries are adapting to new tariffs to better manage their electricity network and avoid unnecessary capacity expansion, mostly because of different heating (heat pumps) and transport (EV). 
We believe this is, in general, the right approach, but it will cause a lot of surprises among consumers who are not technically aware.
This project is here to help you decide how to move forward; we will try to emulate many scenarios and present several solutions while doing calculations involving batteries, solar, and maybe other options in the future.

We'll try to keep the parameters of the calculations as customizable as possible, especially the prices of certain components, from where the calculations will be made. 

Since the authors live in Slovenia, we'll cover the situation here first. You are, of course, all invited to join in and add support for other markets.

## Features

This project has the following ambitions:
- Given 15-minute consumption data for your meter, calculate costs with different "agreed power" (slovenian: dogovorjena moč) values. 
- Calculate the best value for "agreed power" in each interval
- Calculate the best "agreed power" if we introduce a battery, also considering the price of the battery and expected lifetime and expected cycles.
- provide API for the evcc.io and other projects so that cost data provided as a day-ahead price will include the tariff for the transport and battery costs.

  
