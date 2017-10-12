import scrapy


class QuotesSpider(scrapy.Spider):
    name = "quotes"

    base_url = 'https://www.transfermarkt.com/laliga/transfers/wettbewerb/ES1/plus/?saison_id={year}&s_w=&leihe=0&leihe=1&intern=0&intern=1'

    years = range(2010, 2020)

    start_urls = [base_url.format(year=year) for year in years]

    def parse(self, response):
        year = response.url.split("=")[1][:4]
        filename = 'year-%s.html' % year
        with open(filename, 'wb') as f:
            f.write(response.body)


    teams = response.css('.table-header')[1:]
    team_names = [team.get().split('>')[-3][:-3] for team in teams]

    tables = response.css('table')[3:]
    response.css('table/tr')


def parsetable(table):
    table_header = table.css('tr')[0]
    table_header_values = table_header.css('th')
    table_header_values = map(lambda x: x.split('>')[-1][:-4], table_header_values)

    table_rows = table.css('tr')[1:]


