from bs4 import BeautifulSoup
import urllib
import re

def main():
    get_rankings()

def get_rankings():
    html = urllib.urlopen("http://www.cbssports.com/collegefootball/rankings").read()
    soup = BeautifulSoup(html)
    team_list = soup.find_all("td", attrs={"align": "left"})
    rankings = []

    for team in team_list:
        rankings.append(str(team.text))

    fsu_rankings = [i for i, team in enumerate(rankings) if team.endswith('Florida State')]

    return rankings.pop(fsu_rankings.pop(2))[0]

if __name__ == "__main__":
    main()
