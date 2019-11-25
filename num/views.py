import json
from django.shortcuts import render
from django.views import View
from django.http import HttpResponse
# Create your views here.

class NumToWordsView(View):
    def get(self, request):
        body = None
        if request.body:
            body = json.loads(request.body)
        status = 'yes'
        english = ''

        if body and not 'number' in body:
            status = 'no'
        elif body:
            english = to_words(body['number'])
        else:
            status = 'no'

        response = {
            'status': status
        }

        if english:
            response['number_in_english'] = english

        return HttpResponse(json.dumps(response))


def to_words(num):
    under_20 = ['zero', 'one', 'two', 'three', 'four', 'five', 'six', 'seven',
        'eight', 'nine', 'ten', 'eleven', 'twelve', 'thirteen', 'fourteen',
        'fifteen', 'sixteen', 'seventeen', 'eighteen', 'nineteen'
        ]
    tens = ['twenty', 'thirty', 'fourty', 'fifty', 'sixty', 'seventy', 'eighty',
        'ninety'
        ]
    identifier = { 0: '', 1: 'thousand', 2: 'million', 3: 'billion',
        4: 'trillion', 5: 'quadrillion' }

    places = [ num % 1000 ]

    while num >= 1000:
        num = num // 1000
        places.append(num % 1000)

    name = ""

    def zero_filter(num, modulo):
        return ' ' + under_20[num % modulo] if under_20[num % modulo] != 'zero'\
        else ''

    for i, s in reversed(list(enumerate(places))):
        if i == 0:
            name += ' '
        if s < 20:
            name += under_20[s]
        elif s < 100:
            name += tens[s // 10 - 2]\
            + zero_filter(s, 10)
        else:
            name += under_20[s // 100] + ' hundred'\
            + (zero_filter(s, 100) if s % 100 < 20 else ' '\
            + tens[(s % 100) // 10 - 2] + zero_filter(s, 10))

        name += ' ' + identifier[i] if identifier[i] else ''
    return name
