import time
from urllib.request import urlopen, Request
import json
import re
from bs4 import BeautifulSoup as BS

from .models import Tenant


def parse_blacklist():
    c = 1
    while True:
        response = Request('https://listblacks.com/swindlers?page=%s' % c, headers={'User-Agent': 'Mozilla/5.0'})
        web = urlopen(response)
        soup = BS(web.read(), 'lxml')
        tag = soup.find("div", {'class': 'container-fluid'})
        data = str(tag.find_all('script')[1].string).split('\n')
        swindlers_str = data[3].replace(' swindlers:', '')[:-1]
        swindlers = json.loads(swindlers_str)
        if len(swindlers) < 1:
            break
        c = c + 1
        for i in swindlers:
            try:
                if not i['phone']:
                    continue
                elif i['phone'] == '':
                    continue
                phone = i['phone'].replace('(', '').replace(')', '').replace('+', '').replace('-', '').replace(' ', '')
                if phone[0] == '8' and len(phone) > 10:
                    phone = re.sub('8', '7', phone, 1)
                if Tenant.objects.filter(phone=phone, phone__isnull=False).exists():
                    tn = Tenant.objects.get(phone=i['phone'])
                    m = re.match(i['description'], tn.comment)
                    if not m:
                        tn.comment = i['description'] + '\n' + tn.comment
                    tn.blacklist = True
                    tn.save()
                    continue
                tenant = Tenant()
                tenant.user = None
                tenant.name = i['name']
                tenant.phone = phone
                tenant.comment = i['description']
                tenant.blacklist = True
                tenant.save()
            except Exception as e:
                print(e.__str__())
        Tenant.objects.filter(phone__isnull=True).delete()


def parse_forever():
    while True:
        parse_blacklist()
        time.sleep(86400)
