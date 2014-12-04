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
    
    current_cfp_ranking = rankings.pop(fsu_rankings.pop(2))[0]
    print current_cfp_ranking
    return current_cfp_ranking

if __name__ == "__main__":
    main()
