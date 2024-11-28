## SWDE case study

### Data:
* Tabular data for each time instance in the pressure measurements spreadsheet
* The number of active meters (measurements), is 40 - the last column in the No_og_loggers_at_tomes.

The maximum no of loggers is 40. If there is 40 active loggers logging at 15 minutes intervals, we can assume that the average value is represented by the particular meter. Ther will w be only one blank for the first 15 minutes (only 39 meters active). It is not a problem we can leave blank in the e-FAVOR spreadsheet and I will think how to fill it later. I hope that this simplify the program with the fixed no of meters (loggers).

### Workflow:
We need two files:
1. Logger file
