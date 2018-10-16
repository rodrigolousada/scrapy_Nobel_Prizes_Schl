''' This code still can't exclude some cases like "(physisist)", "(postdoc)", "[1]", "(1986)" and "(", due to Wikipedia html inconsistencies! It's faster if you clean manueally'''

import scrapy

class NobelSpider(scrapy.Spider):
    name = 'nobel'
    start_urls = [
        'https://en.wikipedia.org/wiki/List_of_Nobel_laureates_in_Chemistry',
        'https://en.wikipedia.org/wiki/List_of_Nobel_laureates_in_Physics',
    ]

    def parse(self, response):
        body = response.xpath('//*[@id="mw-content-text"]/div/table/tbody')
        dic = {}
        for winner in body:
            dic.update({
                'winners': winner.xpath('///th/a//text()').extract(),
                'urls': winner.xpath('///th/a/@href').extract(),
            })
        for i in range(len(dic['winners']) - 2):
            yield response.follow('https://en.wikipedia.org' + dic['urls'][i], self.parse_advisors)

    def parse_advisors(self, response):
        body = response.xpath('//*[@id="mw-content-text"]/div/table[@class="infobox biography vcard"]/tbody')

        advisor_list = body.xpath('///tr[contains(.,"Doctoral advisor")]/td/a//text()').extract() + \
                        body.xpath('///tr[contains(.,"Doctoral advisor")]/td/text()').extract() + \
                        body.xpath('///tr[contains(.,"Academic advisors")]/td/text()').extract() + \
                        body.xpath('///tr[contains(.,"Academic advisors")]/td/a//text()').extract() + \
                        body.xpath('///tr[contains(.,"Other academic advisors")]/td/text()').extract() + \
                        body.xpath('///tr[contains(.,"Other academic advisors")]/td/a//text()').extract()
        students_list = body.xpath('///tr[contains(.,"Notable students")]/td/a//text()').extract() + \
                        body.xpath('///tr[contains(.,"Notable students")]/td/text()').extract() + \
                        body.xpath('///tr[contains(.,"Doctoral students")]/td/text()').extract() + \
                        body.xpath('///tr[contains(.,"Doctoral students")]/td/a//text()').extract() + \
                        body.xpath('///tr[contains(.,"Other notable students")]/td/text()').extract() + \
                        body.xpath('///tr[contains(.,"Other notable students")]/td/a//text()').extract()
        institutions_list = body.xpath('///tr[contains(.,"Institutions")]/td//*/a//text()').extract() + \
                        body.xpath('///tr[contains(.,"Institutions")]/td//*/text()').extract()
        advisor_clean = [x.strip().replace(',','') for x in advisor_list if "postdoc" not in x]
        advisor_clean = list(filter(None, advisor_clean))
        students_clean = [x.strip().replace(',','') for x in students_list if "postdoc" not in x]
        students_clean = list(filter(None, students_clean))
        institutions_clean = [x.strip().replace(',','') for x in institutions_list if "postdoc" not in x]
        institutions_clean = list(filter(None, institutions_clean))
        yield {
            'name': response.xpath('//*[@id="firstHeading"]/text()').extract_first(),
            # 'name2': response.xpath('//*[@id="mw-content-text"]/div/table[@class="infobox biography vcard"]/tbody/tr[1]/th/span/text()').extract_first()
            'advisors': advisor_clean,
            'students': students_clean,
            'institutions': institutions_clean
        }

        # #TO DEBUG FIRST PARSE

        # #1)
        # start_urls = [
        #   'https://en.wikipedia.org/wiki/Jacobus_Henricus_van_%27t_Hoff',
        #   'https://en.wikipedia.org/wiki/Emil_Fischer',
        #   'https://en.wikipedia.org/wiki/William_E._Moerner',
        #   'https://en.wikipedia.org/wiki/Theodor_Svedberg',
        #   'https://en.wikipedia.org/wiki/Heinrich_Otto_Wieland',
        #   'https://en.wikipedia.org/wiki/Greg_Winter',
        # ]

        # #2)
        # def parse(self, response):
        #     #body = response.xpath('//*[@id="mw-content-text"]/div/table[1]/tbody')
        #     body = response.xpath('//*[@id="mw-content-text"]/div/table/tbody')
        #     dic = {}
        #     for winner in body:
        #         dic.update({
        #             #'year' : winner.xpath('///td[1]//text()').extract(),
        #             'winners': winner.xpath('///th/a//text()').extract(),
        #             'urls': winner.xpath('///th/a/@href').extract(),
        #         })
        #     print(" winner " + str(len(dic['winners'])) + " url " +str(len(dic['urls'])))
        #     for i in range(len(dic['winners']) - 2):
        #         yield {
        #             'winner': dic['winners'][i],
        #             'url': 'https://en.wikipedia.org' + dic['urls'][i]
        #         }
