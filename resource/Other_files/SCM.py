Meet - boc-vonq-pfb (google.com)
*case of drug misuse
use "/Users/jeffrey/Desktop/stata/drug_good.dta", clear
drop drugalcoholinducedcause
rename drugalcoholinducedcausecode cases
collapse (sum) case = cases, by(state year)
save "/Users/jeffrey/Desktop/stata/case_good.dta", replace



*Aggregated Date
clear
use "/Users/jeffrey/Desktop/stata/stata_data_good.dta"
merge m:1 state year using 18to24_good.dta
drop _merge
merge m:1 state year using poverty_good.dta
drop _merge
merge m:1 state year using GDP_good.dta
drop _merge
merge m:1 state year using dummy_good.dta
drop _merge
merge 1:m state year using case_good.dta
drop _merge
drop if (year == 2020) | state == "DISTRICT OF COLUMBIA"
save "/Users/jeffrey/Desktop/stata/QQ.dta", replace



*Synthetic Control
use QQ.dta
sort state year
rename population18to24years Y18to24
encode state, generate(state_new)
drop state
rename state_new state
order state year, first
label variable dummy_clean  "legalized next year"
label variable dummy_real  "legalized exact year"
gen rate_vio = violence / population 
gen rate_pro = property / population
gen crime_rate = (violence + property) / population 
save "/Users/jeffrey/Desktop/stata/QAQ.dta", replace



1 RESEARCH QUESTION 

My research is to discuss whether the legalization of recreational marijuana could decrease the crime rate on violence or on property in aggregate level data by states in the USA from 1999 to 2019.
The treatment variable is intuitively defined as the time (year) when the court enacted the law of recreational use marijuana.
The outcome variables in this research are the cases of violence crimes and property crimes in the given states and years. Both of the figures are defined as the summary of various crimes in the list according to the FBI which are somehow closely related to drug use.
Potential outcome framework :

Define for dummy variable (treatment effect)

Di =1, if state i treated legal use of recreational marijuana 
Di =0, if state i  not treated legal use of recreational marijuana 

Define for outcomes variable (crime rate)

Yi1 =1, potential outcome for state i if getting treated 
Yi1 =0, potential outcome for state i if not getting treated 

Observed outcomes

Yi =Yi1 Di +Yi0 (1 - Di) 

We wish to estimate the causal effect as

 =Yi1  - Yi0  

However, there exists a counterfactual scenario.

 =E(Yi | Di =1) -E(Yi | Di =0)  
 =E(Yi1 | Di =1) -E(Yi0 | Di =1)+E(Yi0 | Di =1) -E(Yi0 | Di =0)  
 =ATT +selection bias 

 

2 CREATE SAMPLE FOR ANALYSIS: PART 2

*dealing with the data set for “cases of drug misuse”

use "/Users/jeffrey/Desktop/stata/drug_good.dta", clear
drop drugalcoholinducedcause
rename drugalcoholinducedcausecode cases
collapse (sum) case = cases, by(state year)
save "/Users/jeffrey/Desktop/stata/case_good.dta", replace

clear
use temp_data.dta
append using 1999_good.dta
sort state year
save "/Users/jeffrey/Desktop/stata/temp_data01.dta", replace

*integrate the whole data and generate the crime_rate

clear
use "/Users/jeffrey/Desktop/stata/stata_data_good.dta"
merge m:1 state year using 18to24_good.dta
drop _merge
merge m:1 state year using poverty_good.dta
drop _merge
merge m:1 state year using GDP_good.dta
drop _merge
merge m:1 state year using dummy_good.dta
drop _merge
merge 1:m state year using case_good.dta
drop _merge
drop if (year == 2020) | state == "DISTRICT OF COLUMBIA"
save "/Users/jeffrey/Desktop/stata/QQ.dta", replace

clear
use QQ.dta
sort state year
rename population18to24years Y18to24
encode state, generate(state_new)
drop state
rename state_new state
order state year, first
label variable dummy_clean  "legalized next year"
label variable dummy_real  "legalized exact year"
gen rate_vio = violence / population 
gen rate_pro = property / population
gen crime_rate = (violence + property) / population 
save "/Users/jeffrey/Desktop/stata/QAQ.dta", replace
3 VISUALIZE DATA
*histogram

histogram property, freq 
histogram violence, freq 

As we examine the histogram of violence crime and property crime, we can find out that both graphs seem to be exponentially distributed with coefficient lambda not so small. Which are not so different from the theoretical point of view.
On the other hand, we examine the income (median household income in given states and years)
histogram income, freq normal kdensity title ("different distribution")
We can discover that the density of income is skewed to the right compared to the normal distribution, which also coincides with the theoretical point of view.



*graph two way
By intuition, we can say that the variables (rate_vio, rate_pro) and income would be negatively related. As we zoom in the scatter plot of the two kinds of crime rate toward income.

graph twoway scatter rate_vio income
graph twoway scatter rate_pro income

We can further inspect the relationship between crime rate of property and income.
graph twoway (scatter rate_vio income) (lfit rate_vio income), legend(position(6) ring(1) label(1 "violence crime rate") label(2 "fitted value with income"))
We can discover that the relationship between rate_pro and income is stronger than the other one, which coincides with our intuition.


4 PRELIMINARY ANALYSIS
*regression

In this dataset, we have two potential outcome variables which is violence (number of violence crimes during that given year) and property (number of property crimes during that given year). As for the dummy variable, we have dummy_real and dummy_clean. The former one is the time when the state actually legalized the use of recreational marijuana. And as for the latter one, since almost every state enact the law in November, we then set the real time affecting outcome variable as the following year.

*regress outcome variable on different kinds of dummies
reg violence dummy_clean 
reg property dummy_clean 

Both of these two regression models give very poor estimations on dummy variables to the outcome variable for very low t-value (0.23, -0.11)  and R-squared value.
Also, on regressions

*regress outcome variable on different kinds of dummies
reg property dummy_real 
reg violence dummy_real 

show poor results on the estimations, (t-value 0.11, 0.66 respectively) and low R-squared value.
However, after I generate several new variables converting the actual numbers of violence crimes and property crimes into the rate of the crime. We can derive the result of having significant t-value (all at 5% confidence level) but still low value on the R-squared value.
According to the above results, we can draw the conclusion that there exist some incentives for us to convert the number type data into rate type data.


*OVB formula

The above estimation is the channel between outcome variables (crime rates) and treatment variables (legalization). After considering all possible causal effects, the possibility of omitted variable bias problems to occur is quite high. 
From OVB formula

if our TRUE formula :

Yi = a + bDi+ cXi+i

if our ESTIMATED model :

Yi = a + bDi+ui

We can have 

ui= cXi+i

As for OLS for b:

b Cov(Y, D) / Var(D)
b b+Cov(u, D) / Var(D)
b b+cCov(X, D) / Var(D),     where Cov(X, D) 0 

which implies that the OLS estimator for b is biased. Therefore, we introduce the synthetic control method to deal with the omitted variable bias problem.

*Bad control
As one example of one possible bad control variable is the trading violumn for the drugs in black markets. 
Since this number could somehow decrease due to the legalization of recreational usage of marijuana and further decrease the crime rate. 
We should not do any inference on this, otherwise, we could shut down the channel and underestimate the effect on the legalization.

*******************************************************************************************
***Results by year***

COLORADO 		2012		6	UP*		4.66
WASHINGTON 	2012		47	Half		4.58
OREGON 		2014		37	Half&UP	4.36
ALASKA 		2014		2	UP*		7.11

MAINE 		2016		19	LOW*		5.42
NEVADA 		2016		28	(NF)		5.46
CALIFORNIA 		2016		5	UP*		4.83
MASSACHUSETTS 	2016		21	LOW*		6.59

*******************************************************************************************
***Clear type***

COLORADO 		2012		6	UP*		4.66	mid_west	(54%)
WASHINGTON 	2012		47	Half		4.58	north_west	(90%)
OREGON 		2014		37	UP*		4.36	north_west	(66%)
ALASKA 		2014		2	UP**		7.11	north_west_O	(70%)

MAINE 		2016		19	LOW*		5.42	north_east	(10%)
NEVADA 		2016		28	(NF)		5.46	west		(68%)
CALIFORNIA 		2016		5	UP**		4.83	west		(48%)
MASSACHUSETTS 	2016		21	LOW**		6.59	north_east	(26%)

*******************************************************************************************
clear
use QAAQ.dta
tsset state year
synth_runner crime_rate income gdp case poverty(2010(1)2019) Y18to24(2010(1)2019) crime_rate(1999) crime_rate(2001) crime_rate(2003)  crime_rate(2005) crime_rate(2007)  crime_rate(2009) crime_rate(2011) crime_rate(2013) crime_rate(2015) crime_rate(2017)  crime_rate(2019), trunit(6) trperiod(2012) keep("SCM_runner_results") pvals1s pre_limit_mult(5) replace

clear
use QAAQ.dta
tsset state year
merge 1:1 state year using "SCM_runner_results", nogenerate

gen weed_synth = crime_rate - effect

single_treatment_graphs , trlinediff(-1)
effects_ylabels(-30(10)30) effects_ymax(35)

 

Sensitive testing

all rmspe 
.001299 / .0033573
ALA
.0007665 / .0014351

(1999, 2004, 2009, 2014, 2019)
.0015969 / .0021325
ALA
.0011894 / .0007484

all pre(1999 - 2012)
.001299 / .0033573
ALA
.0007665 / .0014351

(1999, 2004, 2009)
.0015028 / .002224
ALA
.0011671 / .0008192

(1999, 2001, 2003, 2005, 2007, 2009, 2011, 2012)
.0014587 / .0025419
ALA
.0009402 / .0007802

(2000, 2004, 2008, 2012)
.0015645 / .002418
ALA
.00125	/ .0013202




*after KAUL*


clear
use QAAQ.dta
tsset state year

gen byte D = (state==6 & year>=2012) | (state==47 & year>=2012) | (state==37 & year>=2014) | (state==2 & year>=2014) | (state==19 & year>=2016) | (state==28 & year>=2016) | (state==5 & year>=2016) | (state==21 & year>=2016)
synth_runner crime_rate income gdp case poverty(2010(1)2019) Y18to24(2010(1)2019) crime_rate(1999) crime_rate(2001) crime_rate(2003) crime_rate(2005) crime_rate(2007) crime_rate(2009) crime_rate(2011) crime_rate(2013) crime_rate(2015), d(D) pvals1s pre_limit_mult(5), trlinediff(-1)