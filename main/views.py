import os
import csv
from decimal import Decimal
from django.template import RequestContext
from django.shortcuts import render_to_response
from main.models import Product
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import redirect


def index(request):
    adult = Product.objects.filter(ADVERTISERCATEGORY='Adult Costumes')[:4]
    kids = Product.objects.filter(ADVERTISERCATEGORY='Kids Costumes')[:4]
    teen = Product.objects.filter(ADVERTISERCATEGORY='Teen Costumes')[:4]
    baby = Product.objects.filter(ADVERTISERCATEGORY='Baby Toddler Costumes')[:4]
    pet = Product.objects.filter(ADVERTISERCATEGORY='Pet Costumes')[:4]
    accessories = Product.objects.filter(ADVERTISERCATEGORY='Costume Accessories')[:4]
    decor = Product.objects.filter(ADVERTISERCATEGORY='Decor Party Supplies')[:4]
    for product in adult:
        product.NAME = rotate_name(product.NAME)
    for product in kids:
        product.NAME = rotate_name(product.NAME)
    for product in teen:
        product.NAME = rotate_name(product.NAME)
    for product in baby:
        product.NAME = rotate_name(product.NAME)
    for product in pet:
        product.NAME = rotate_name(product.NAME)
    for product in accessories:
        product.NAME = rotate_name(product.NAME)
    for product in decor:
        product.NAME = rotate_name(product.NAME)
    context = {'adult': adult, 'kids': kids, 'teen': teen, 'baby': baby, 'pet': pet, 'decor': decor,
               'accessories': accessories}

    return render_to_response('index.html', context, context_instance=RequestContext(request))


def category(request, cat_id, page):
    product_list = Product.objects.filter(ADVERTISERCATEGORY=cat_id.replace('_', ' '))
    paginator = Paginator(product_list, 24)
    try:
        products = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        products = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        products = paginator.page(paginator.num_pages)

    for product in products:
        product.NAME = rotate_name(product.NAME)
    context = {'products': products, 'category': cat_id.replace('_', ' '), 'cat_id': cat_id}
    return render_to_response('category.html', context, context_instance=RequestContext(request))


def import_req(request):
    cwd = os.getcwd()
    file_list = os.listdir(cwd + '/import')
    context = {'file_list': file_list}
    if 'optionsRadios' in request.GET:
        catalog = cwd + '/import/' + request.GET['optionsRadios']
        file_catalog = open(catalog, "rb")
        reader = csv.reader(file_catalog)
        row_num = 0
        rows = []
        for row in reader:
            if row_num == 0:
                header = row
                rows.append(header[20])
            else:
                if not Product.objects.filter(NAME=row[4]):
                    if row[20] == '':
                        cats = ':'.split(':')
                    else:
                        cats = row[20].split(':')
                    if not row_num == 5:
                        rows.append(cats)
                    product = Product(PROGRAMNAME=row[0], PROGRAMURL=row[1], CATALOGNAME=row[2], LASTUPDATED=row[3],
                                      NAME=row[4], KEYWORDS=row[5],
                                      DESCRIPTION=row[6], SKU=row[7], MANUFACTURER=row[8], MANUFACTURERID=row[9],
                                      UPC=row[10], ISBN=row[11], CURRENCY=row[12],
                                      SALEPRICE=Decimal(zero_if_empty(row[13].replace(',', ''))),
                                      PRICE=Decimal(zero_if_empty(row[14].replace(',', ''))),
                                      RETAILPRICE=Decimal(zero_if_empty(row[15].replace(',', ''))),
                                      FROMPRICE=row[16], BUYURL=row[17], IMPRESSIONURL=row[18], IMAGEURL=row[19],
                                      ADVERTISERCATEGORY=cats[0], SUBCATEGORY=cats[1], THIRDPARTYID=row[21],
                                      THIRDPARTYCATEGORY=row[22],
                                      AUTHOR=row[23], ARTIST=row[24], TITLE=row[25], PUBLISHER=row[26], LABEL=row[27],
                                      FORMAT=row[28], SPECIAL=row[29],
                                      GIFT=row[30], PROMOTIONALTEXT=row[31], STARTDATE=row[32], ENDDATE=row[33],
                                      OFFLINE=row[34], ONLINE=row[35],
                                      INSTOCK=row[36], CONDITION=row[37], WARRANTY=row[38],
                                      STANDARDSHIPPINGCOST=Decimal(zero_if_empty(row[39].replace(',', ''))))
                    product.save()
            row_num += 1
        file_catalog.close()
        context['rows'] = rows

    return render_to_response('import.html', context, context_instance=RequestContext(request))


def zero_if_empty(value):
    if value == '':
        return '0'
    return value


def item(request, id):
    product = Product.objects.get(pk=id)
    product.IMAGEURL = product.IMAGEURL.replace('250', '1000')
    product.NAME = rotate_name(product.NAME)
    tags = set(product.KEYWORDS.split(','))
    context = {'product': product, 'category': product.ADVERTISERCATEGORY.replace(' ', '_'), 'tags': tags}
    return render_to_response('item.html', context, context_instance=RequestContext(request))


def get(request, get):
    product = Product.objects.get(pk=get)
    return redirect(product.BUYURL)

def rotate_name(name):
    name_list = name.split()
    name = name_list[-1] + ' ' + ' '.join(name_list[:-2])
    return name