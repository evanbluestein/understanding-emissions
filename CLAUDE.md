# understanding emissions - Data Analysis Project

A portfolio piece analysis of climate change, looking at the sources of emissions, emissions in the atmosphere, the change in global temperature, and how energy generation is changing.

Data is pulled, organized, and analyzed. Charts are generated which are exported into graphics formats for video editing a piece that explains the findings. 

## Stack:

- UV (standardize python version)
- Python (pull data)
- SQLite3 (combine data from sources)
- pandas (analyze data)
- plotly (chart data)
- kaleideo (graphic export)

## Data sources:

1. Who emits	Our World in Data CO₂ dataset (github.com/owid/co2-data, 14 MB)	CO₂ and other greenhouse gases by country and year back to 1750: totals, per person, by fuel, and emissions embedded in imports
2. Where it goes	NOAA Mauna Loa monthly CO₂ (gml.noaa.gov)	CO₂ in the atmosphere, measured monthly since 1958. The famous rising, zigzagging line
3. What it does	NASA GISTEMP global temperature (data.giss.nasa.gov)	Global temperature compared with a 1951–1980 baseline, monthly since 1880
4. What's changing	Our World in Data energy dataset (github.com/owid/energy-data, 9 MB)	Electricity and energy by source for every country: coal, gas, solar, wind, nuclear

## Questions: 

Who's responsible? Rank countries three ways: emissions this year, emissions per person, and total emissions since 1850. The leaderboard changes dramatically depending on which you pick, and that disagreement is at the heart of most climate-policy arguments.

How tightly do emissions, CO₂ and temperature track each other? Cumulative emissions against atmospheric CO₂, then against temperature. The near-straight line between total emissions and warming is the single most clarifying fact in climate science.

Can countries grow without emitting more? Find countries whose GDP rose while their emissions fell (OWID includes GDP), and compare that with the emissions embedded in their imports. It's an honest test of "decoupling."

How fast is the energy switch? Solar and wind's share of electricity, by country, over the last 15 years: who's moving fastest, and is it fast enough?