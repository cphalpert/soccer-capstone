import scrapy
import pandas as pd
import pickle
from itertools import product

class QuotesSpider2(scrapy.Spider):
    name = "quotes"

    base_url = 'https://www.transfermarkt.co.uk/{team_slug}/kader/verein/{team_id}/plus/1/galerie/0?saison_id={year}'
    print 'loaded'
    years = range(2008, 2018)

    teams = [('athletic-bilbao', 621),
            ('atletico-madrid', 13),
            ('ca-osasuna', 331),
            ('cd-leganes', 1244),
            ('cd-numancia', 2296),
            ('cd-teneriffa', 648),
            ('celta-vigo', 940),
            ('deportivo-alaves', 1108),
            ('deportivo-la-coruna', 897),
            ('deportivo-xerez', 134),
            ('espanyol-barcelona', 714),
            ('fc-barcelona', 131),
            ('fc-cordoba', 993),
            ('fc-elche', 1531),
            ('fc-getafe', 3709),
            ('fc-girona', 12321),
            ('fc-granada', 16795),
            ('fc-malaga', 1084),
            ('fc-sevilla', 368),
            ('fc-valencia', 1049),
            ('fc-villarreal', 1050),
            ('hercules-alicante', 7971),
            ('racing-santander', 630),
            ('rayo-vallecano', 367),
            ('rcd-mallorca', 237),
            ('real-betis-sevilla', 150),
            ('real-madrid', 418),
            ('real-saragossa', 142),
            ('real-sociedad-san-sebastian', 681),
            ('real-valladolid', 366),
            ('recreativo-huelva', 2867),
            ('sd-eibar', 1533),
            ('sporting-gijon', 2448),
            ('ud-almeria', 3302),
            ('ud-las-palmas', 472),
            ('ud-levante', 3368)]

    start_urls = []

    for year, team in product(years, teams):
        start_urls.append(base_url.format(year=year, team_slug=team[0], team_id =team[1]))

    def parse(self, response):
        year = response.url.split("=")[1][:4]

        
        
        table = response.css('.items')[0]
        
        team_name = response.url.split("/")[3]

        filename = 'year-%s-%s.p' % (year, team_name)

        table_df = extract_table(table)
        table_df['team_name'] = team_name
        table_df['year'] = year
        
        with open(filename, 'wb') as f:
            pickle.dump(table_df, f)

    

def extract_table(table):
    table_header = table.css('tr')[0]
    table_header_values = table_header.css('th')
    columnns = ['#', 'Player(s)', 'born/age', 'Nat1', 'Nat2', 'Height', 'Foot', 'In the team since', 'before', 'Contract until', 'Market value']

    extracted_rows = []
    table_rows = table.css('tr')[1:]
    for row in table_rows:
        try:
            extracted_rows.append(parse_row(row))
        except:
            pass
    return pd.DataFrame.from_records(columns=columnns, data=extracted_rows)

def parse_row(row):
    row_values = []
    row_values.append(row.select('td')[0].select("div/text()").get()) # Rank
    row_values.append(row.select('td')[1].select("table//a/img/@title").get()) # Name
    row_values.append(row.select('td')[2].select("text()").get()) # Birthday
    row_values.append(row.select('td')[3].select("img//@title").get()) # nationality
    row_values.append(row.select('td')[4].select("a//img/@alt").get()) # nation2
    row_values.append(row.select('td')[5].select('text()').get()) # height
    row_values.append(row.select('td')[6].select('text()').get()) # foot
    row_values.append(row.select('td')[7].select('text()').get()) # start
    row_values.append(row.select('td')[8].select('a//img/@alt').get()) # From
    row_values.append(row.select('td')[9].select('text()').get()) # Contract until
    row_values.append(row.select('td')[10].select('text()').get()) # value
    return row_values



# Run this to go into shell interactive mode:
# scrapy shell "https://www.transfermarkt.co.uk/real-madrid/kader/verein/418/plus/1/galerie/0?saison_id=2008"

# Scrapy examples: https://docs.scrapy.org/en/latest/intro/tutorial.html


