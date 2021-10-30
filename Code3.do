clear all
/*Append all the files*/
cd "C:\Users\Lenovo\Desktop\RA\df_1"
fs df_1_*.dta
foreach file in `r(files)'{
	append using `file'
}
sort id_lender
drop if lat == .

global NUM = _N
drop index
gen index = _n
cd "C:\Users\Lenovo\Desktop\RA\data"
save temp_, replace // save the file cleaned as temp.dta

/*Deal with the file aq.dta.*/
use "aq_uniq_location", clear
drop if Latitude == .
gen id_ = _n
drop city State st
*ren city city_aq
*ren State State_aq
expand $NUM
bys id_: gen t = _n
sort t id_ /*Sort data by t(# of group) at first, and then sort data in each group.*/
gen index = t
drop id_ t

/*Merge two files above*/
merge m:1 index using temp_
drop _merge
order id_lender city State lat lon

/*Compute the distance (kilometers), and then map each lender to the nearest station.*/
geodist lat lon Latitude Longitude , generate(distance)
save temp_2, replace
collapse (min) distance, by(id_lender)
ren distance distance_min
merge 1:m id_lender using temp_2
keep if distance == distance_min
drop _merge index Latitude Longitude distance_min
cd "C:\Users\Lenovo\Desktop\RA\save_temp"
save "aq", replace

keep if distance <= 100
hist distance


/*Deal with the file weather_uniq_location.dta.*/
cd "C:\Users\Lenovo\Desktop\RA\data"
use "weather_uniq_location", clear
drop if Latitude == .
gen id_ = _n
drop DISTRICT STATE
replace Latitude = Latitude / 10000
replace Longitude = Longitude / 10000
*ren city city_aq
*ren State State_aq
expand $NUM
bys id_: gen t = _n
sort t id_ /*Sort data by t(# of group) at first, and then sort data in each group.*/
gen index = t
drop id_ t

/*Merge two files above*/
merge m:1 index using temp_
drop _merge
order id_lender city State lat lon

/*Compute the distance (kilometers), and then map each lender to the nearest station.*/
geodist lat lon Latitude Longitude , generate(distance)
save temp_2, replace
collapse (min) distance, by(id_lender)
ren distance distance_min
merge 1:m id_lender using temp_2
keep if distance == distance_min
drop _merge index Latitude Longitude distance_min
cd "C:\Users\Lenovo\Desktop\RA\save_temp"
save "weather", replace

// keep if distance <= 100
// hist distance


/*Deal with the file aq.dta.*/
cd "C:\Users\Lenovo\Desktop\RA\data"
use "noise_uniq_location", clear
drop if lat == .
gen id_ = _n
ren lat lat_noise
ren lon lon_noise
keep id_ stnid lat lon
*ren city city_aq
*ren State State_aq
expand $NUM
bys id_: gen t = _n
sort t id_ /*Sort data by t(# of group) at first, and then sort data in each group.*/
gen index = t
drop id_ t

/*Merge two files above*/
merge m:1 index using temp_
drop _merge
order id_lender city State lat lon

/*Compute the distance (kilometers), and then map each lender to the nearest station.*/
geodist lat lon lat_noise lon_noise , generate(distance)
save temp_2, replace
collapse (min) distance, by(id_lender)
ren distance distance_min
merge 1:m id_lender using temp_2
keep if distance == distance_min
drop _merge index lat_noise lon_noise distance_min
cd "C:\Users\Lenovo\Desktop\RA\save_temp"
save "noise", replace




*-------TEST CODE BELOW------*

/*Deal with the file df_1_X_to_Y.dta.*/
/*cd "C:\Users\Lenovo\Desktop\RA\Crawl"
use df_1_1_104.dta, clear
global NUM = _N
drop index
gen index = _n
cd "C:\Users\Lenovo\Desktop\RA\data"
save temp_, replace // save the file cleaned as temp.dta

/*Deal with the file aq.dta.*/
use "aq_uniq_location", clear
drop if Latitude == .
gen id_ = _n
drop city State st
*ren city city_aq
*ren State State_aq
expand $NUM
bys id_: gen t = _n
sort t id_ /*Sort data by t(# of group) at first, and then sort data in each group.*/
gen index = t
drop id_ t

/*Merge two files above*/
merge m:1 index using temp_
drop _merge
order id_lender city State lat lon

/*Compute the distance (kilometers), and then map each lender to the nearest station.*/
geodist lat lon Latitude Longitude , generate(distance)
save temp_2, replace
collapse (min) distance, by(id_lender)
merge 1:1 id_lender distance using temp_2
keep if _merge == 3
drop _merge index Latitude Longitude*/






