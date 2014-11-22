import requests
from lxml import html
import unicodecsv
import os
import xlwt
import parser


def get_page(site, base_url):
    r = requests.get(site)
    dom = html.fromstring(r.content)
    dom.make_links_absolute(base_url=base_url)
    return r.status_code, dom

# build skeleton parser for websites!
# class parser()
# class Forbes(parser)
# class Reuters(parser)
# class Bloomberg(parser)
# class SEC(parser)
# parsing templates!
# getting semi-structured data out automatically
# tables should be the easiest
# then H1|H2|H3 and children
#

def get_info(CIK, type_='DEF'):
    #site = r'http://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&CIK=0000320193&type=DEF'
    site = r'http://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&CIK={0}&type={1}'.format(CIK, type_)

    status_code, dom = get_page(site, base_url='http://www.sec.gov')
    par = parser.DomParser(dom)
    # for url in par.links:
    #     print url

    par.data = 'title'
    par.selector = 'span.companyName'
    title = par.parserText()
    #print title

    par.data = 'info'
    par.selector = 'p.identInfo'
    info = par.parserText()[par.data]
    try:
        info = info.replace('formerly', '|formerly').replace('State location', '|State location').replace('(Assistant Director Office: 3)', '|(Assistant Director Office: 3)|').split('|')
    except Exception, e:
        print e
        info = info.split('|')
    #print info

    par.data = 'addresses'
    par.selector = 'div.mailer'
    addresses = par.parserText()
    mailing = [x.strip() for x in addresses['addresses'][0].split('\n')]
    business = [x.strip() for x in addresses['addresses'][1].split('\n')]
    #print mailing
    #print business

    filings = par.parserTable(['Filings', 'Format_text', 'Description', 'Filing_Date', 'File/Film_Number'])
    filings_ = [['Filings', 'Format_text', 'Format_URL', 'Description', 'Filing_Date', 'File/Film_Number', 'File/Film_Number_url']]
    for file_ in filings:
        filings_.append([x.strip() for x in file_])

    return [(title, mailing, business)], [info], filings_


def write_to_excel(title, main_data, filings_data, other_data=None):
    workbook = xlwt.Workbook()
    main_sheet = workbook.add_sheet('main')
    other_sheet = workbook.add_sheet('other')
    filings_sheet = workbook.add_sheet('filings')

    for index, value in enumerate(main_data):
        for i2, v2 in enumerate(value):
            #print [v2]
            main_sheet.write(index, i2, v2)

    for index, value in enumerate(filings_data):
        for i2, v2 in enumerate(value):
            #print [v2]
            filings_sheet.write(index, i2, v2)

    for index, value in enumerate(other_data):
        for i2, v2 in enumerate(value):
            #print [v2]
            other_sheet.write(index, i2, v2)

        #other_sheet.write(0, index, value)

    workbook.save(r'E:\Development\Projects\NU_Projects\FY15\Company_Data\DEF14As\{0}.xls'.format(title))


# DEF14A | 10K | Form-4 | 8K | Form D
# create SEC data folder
# create SIC folder
# create filetype folder
# insert stuff into file

def get_CIKs():
    CIKs = r'E:\Development\Projects\NU_Projects\FY15\Company_Data\cik_ticker.csv'
    with open(CIKs, 'rb') as fin:
        rdr = unicodecsv.reader(fin)
        for row in rdr:
            rowh = [['CIK', 'symbol', 'name', 'exchange', 'sic', 'business', 'incorporated', 'IRS']]
            row = row[0].split('|')

            CIK = row[0]
            if CIK != 'CIK':

                symbol = row[1]
                name_ = row[2]
                Exchange = row[3]
                SIC = row[4]
                Business = row[5]
                Incorporated = row[6]
                IRS = row[7]
                print CIK, name_
                #site = r'http://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&CIK={0}&type=DEF'.format(CIK)
                [(title, mailing, business)], info, filings = get_info(CIK, type_='DEF')
                info.append([title['title']])
                info.append(mailing)
                info.append(business)
                rowh.append(row)
                write_to_excel(CIK + '_' + name_.replace(' ', '_'), rowh, filings, other_data=info)

#get_CIKs()
