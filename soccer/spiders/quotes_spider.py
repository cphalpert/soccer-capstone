import scrapy
import pandas as pd
import pickle


class QuotesSpider(scrapy.Spider):
    name = "quotes"

    base_url = 'https://www.transfermarkt.com/laliga/transfers/wettbewerb/ES1/plus/?saison_id={year}&s_w=&leihe=0&leihe=1&intern=0&intern=1'

    years = range(2008, 2018)

    start_urls = [base_url.format(year=year) for year in years]

    def parse(self, response):
        year = response.url.split("=")[1][:4]
        filename = 'year-%s.p' % year

        teams = response.css('.table-header')[1:]
        team_names = [team.get().split('>')[-3][:-3] for team in teams]


        doubled_team_names = [x for pair in zip(team_names,team_names) for x in pair]

        tables = response.css('table')[3:]


        extracted_tables = []

        for team_name, table in zip(doubled_team_names, tables):
            table_df = extract_table(table)
            table_df['team_name'] = team_name
            table_df['year'] = year
            extracted_tables.append(table_df)

        with open(filename, 'wb') as f:
            pickle.dump(extracted_tables, f)

        print len(extracted_tables)

def extract_table(table):
    table_header = table.css('tr')[0]
    table_header_values = table_header.css('th')
    table_header_values = map(lambda x: x.get().split('>')[-2][:-4], table_header_values)
    table_header_values = table_header_values[:7] + ['Country'] + [table_header_values[7]]
    extracted_rows = []
    table_rows = table.css('tr')[1:]
    for row in table_rows:
        extracted_rows.append(parse_row(row))
    return pd.DataFrame.from_records(columns=table_header_values, data=extracted_rows)

def parse_row(row):
    row_values = []
    row_values.append(row.select('td')[0].select("div//a/@title").get()) # Name
    row_values.append(row.select('td')[1].select("text()").get()) # Agex
    row_values.append(row.select('td')[2].select("img/@title").get()) # Natx
    row_values.append(row.select('td')[3].select("text()").get()) # Position
    row_values.append(row.select('td')[4].select("text()").get()) # Position 2
    row_values.append(row.select('td')[5].select("text()").get()) # mkt value
    row_values.append(row.select('td')[6].select("a//img/@alt").get()) # Other Team
    row_values.append(row.select('td')[7].select("img/@title").get()) # Other Team country
    row_values.append(row.select('td')[8].select("a/text()").get()) # Transfer Value
    return row_values


# Run this to go into shell interactive mode:
# scrapy shell "https://www.transfermarkt.com/laliga/transfers/wettbewerb/ES1/plus/?saison_id=2010&s_w=&leihe=0&leihe=1&intern=0&intern=1"

# Scrapy examples: https://docs.scrapy.org/en/latest/intro/tutorial.html


