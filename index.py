from flask import Flask, render_template, current_app
import urllib
import re
from bs4 import BeautifulSoup
from rankings import get_rankings

app = Flask(__name__)

@app.route("/")
def hello():
    return get_html()

def wins():
    html = urllib.urlopen("http://www.fbschedules.com/ncaa-14/acc/2014-florida-state-seminoles-football-schedule.php").read()
    soup = BeautifulSoup(html)
    result = soup.find('td', attrs={'class': 'maroon'})
    current_wins = result.text
    re_wins = re.search('(..)-(.)', current_wins)
    season_record = re_wins.group(0)
    return season_record

def streak():
    season_wins = wins()
    totalArr = re.search('(..)', season_wins)
    lossesArr = re.findall('(.)', season_wins)
    losses = lossesArr.pop(3)
    total = totalArr.group(0)
    streak_wins = int(total) + 16
    streak_record = str(streak_wins) + "-" + losses
    return streak_record

def determine_if_lost():
    season_record = wins()
    lossesArr = re.findall('(.)', season_record)
    losses = lossesArr.pop(3)
    if int(losses) > 0:
        return "<div style=\"color: red;\">YES</div>"
    else:
        return "<div style=\"color: green;\">NO</div>"

def get_html():
    season_record = wins()
    streak_record = streak()
    lost = determine_if_lost()
    ranking = get_rankings()
    days_since_lost = countdown_script()
    return "<!DOCTYPE html><html><head><style>*{font-family: Arial, sans-serif;text-align: center;position: relative;}.top_title{font-size:50pt;top: 5%;}.big_text{font-size: 300pt;top: 25%;}.record{font-size: 50pt;top: 40%;}</style><title>Has FSU Lost Yet?</title></head><body><div class=\"top_title\">Has FSU Lost Yet?</div><div class=\"big_text\"><b>" + lost + "</b></div><div class=\"record\" id =\"winningStreak\">Winning Streak: " + streak_record + "</div><div class=\"record\" id=\"thisSeason\">This Season: " + season_record + "</div><div class=\"record\">College Football Playoff Ranking: " + ranking + "</div>" + days_since_lost + "<script>(function(i,s,o,g,r,a,m){i['GoogleAnalyticsObject']=r;i[r]=i[r]||function(){(i[r].q=i[r].q||[]).push(arguments)},i[r].l=1*new Date();a=s.createElement(o),m=s.getElementsByTagName(o)[0];a.async=1;a.src=g;m.parentNode.insertBefore(a,m)})(window,document,'script','//www.google-analytics.com/analytics.js','ga');ga('create', 'UA-56656391-1', 'auto');ga('require', 'displayfeatures');ga('send', 'pageview');</script></body></html>"

def countdown_script():
    season_record = wins()
    lossesArr = re.findall('(.)', season_record)
    losses = lossesArr.pop(3)
    if int(losses) > 0:
        return """<script>
               var montharray=new Array("Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec")

               function countup(yr,m,d){
               var today=new Date()
               var todayy=today.getYear()
               if (todayy < 1000)
               todayy+=1900
               var todaym=today.getMonth()
               var todayd=today.getDate()
               var todaystring=montharray[todaym]+" "+todayd+", "+todayy
               var paststring=montharray[m-1]+" "+d+", "+yr
               var difference=(Math.round((Date.parse(todaystring)-Date.parse(paststring))/(24*60*60*1000))*1)
               difference+=""
               document.write("<div class=\\"record\\">Days since last loss: " + difference + "</div>")
               }
               //enter the count up date using the format year/month/day
               countup(2014,12,06)
               </script>"""
    else:
        return """<script>
               var montharray=new Array("Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec")

               function countup(yr,m,d){
               var today=new Date()
               var todayy=today.getYear()
               if (todayy < 1000)
               todayy+=1900
               var todaym=today.getMonth()
               var todayd=today.getDate()
               var todaystring=montharray[todaym]+" "+todayd+", "+todayy
               var paststring=montharray[m-1]+" "+d+", "+yr
               var difference=(Math.round((Date.parse(todaystring)-Date.parse(paststring))/(24*60*60*1000))*1)
               difference+=""
               document.write("<div class=\\"record\\">Days since last loss: " + difference + "</div>")
               }
               //enter the count up date using the format year/month/day
               countup(2012,11,24)
               </script>"""

if __name__ == "__main__":
    app.debug = True
    app.run()
