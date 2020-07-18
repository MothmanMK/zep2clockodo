# zep2clockodo

This project is meant for personal exercise in python and REST API calls.
The code is already fully functional but will be rewritten several times for training.

<p>
<b>Function</b><br>
Reports from the android app Zeiterfassung Pro will be written to the time recording tool Clockodo via it's API
<p>
<b>How to use</b><br>
All files have to be in the same directory.<br>
After successfull upload of times to clockodo the xls file will be deleted.

1. Enter you information in config.ini
2. Enter you times from ZEP to in the xls file or make your own report accordingly
3. Install python3 and the libraries pandas and requests
4. Execute "python3 zep2clockodo.py"

<p>
<b>Related services</b>

https://www.clockodo.com/de/
<br>
https://dynamicg.ch/timerecording/home_en.html
<br>
https://play.google.com/store/apps/details?id=com.dynamicg.timerecording.pro&hl=de
