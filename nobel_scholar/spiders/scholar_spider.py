import scrapy
import csv

class QuotesSpider(scrapy.Spider):
    name = "scholarExtract"

    def start_requests(self):
        urls = [
            # 'https://scholar.google.com/citations?user=qc6CJjYAAAAJ&hl=en',
            # 'https://scholar.google.com/citations?user=qj74uXkAAAAJ&hl=en',
            'https://scholar.google.com/citations?user=7fhGnVEAAAAJ&hl=en&oi=ao',]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    # start_requests = [
    #         'https://scholar.google.com/citations?user=qc6CJjYAAAAJ&hl=en',
    #         'https://scholar.google.com/citations?user=qj74uXkAAAAJ&hl=en'
    #     ]
        
    def parse(self, response):
        columns = {}
        for row in response.xpath('body'):
            columns.update({
                'Name' : row.xpath('//*[@id="gsc_prf"]/div[2]/div[1]//text()').extract_first(),
                'Afiliation' : row.xpath('//*[@id="gsc_prf"]/div[2]//text()').extract_first(),
                'Citations' : row.xpath('//*[@id="gsc_rsb_st"]//tbody/tr[1]/td[2]//text()').extract_first(),
                'h-index' : row.xpath('//*[@id="gsc_rsb_st"]//tbody/tr[2]/td[2]//text()').extract_first(),
            })
        
        coauthors, allcoauthors = [], response.xpath('//*[@class="gsc_rsb_a"]')
        for author in allcoauthors :
            coauthors +=  author.xpath('.//a//text()').extract()
        columns.update({'co-authors': coauthors})
        write_dict_to_csv('csv.csv',[*columns], columns )        


def write_dict_to_csv(csv_file, csv_columns, dict_data): 
    #ToDo: resolver o problema de imprimir por cima do csv ja criado 
    try:
        with open(csv_file, 'w') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=csv_columns)
            writer.writeheader()
        
            writer.writerow(dict_data)
    except IOError:
        print("I/O error", csv_file)
    return



# columns = {}
#         for row in response.xpath('body'):
#             columns.update({
#                 'Name' : row.xpath('//*[@id="gsc_prf"]/div[2]/div[1]//text()').extract_first(),
#                 'Afiliation' : row.xpath('//*[@id="gsc_prf"]/div[2]//text()').extract_first(),
#                 'Citations' : row.xpath('//*[@id="gsc_rsb_st"]//tbody/tr[1]/td[2]//text()').extract_first(),
#                 'h-index' : row.xpath('//*[@id="gsc_rsb_st"]//tbody/tr[2]/td[2]//text()').extract_first(),
#             })
#         coauthors, allcoauthors = [], response.xpath('//*[@class="gsc_rsb_a"]')
#         for author in allcoauthors :
#             coauthors.append( author.xpath('.//a//text()').extract())

#         columns.update({'co-authors' : coauthors[0]})
#         print(columns)

   

       
       