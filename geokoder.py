import urllib.request
import urllib.parse
import json

def geocode(miasto, ulica, numer, kod):
    service = "http://services.gugik.gov.pl/uug/?"
    params = {"request":"GetAddress", "address":"%s, %s %s" % (miasto, ulica, numer)}
    paramsUrl = urllib.parse.urlencode(params, quote_via=urllib.parse.quote_plus)
    request = urllib.request.Request(service + paramsUrl)
    # print(service + paramsUrl)
    response = urllib.request.urlopen(request).read()
    js = response.decode("utf-8") #pobrany, zdekodowany plik json z odpowiedzia z serwera
    w = json.loads(js)

    try:
        results = w['results']
        if not results: #jeżeli jest pusta lista z wynikami
            return None
        elif kod == '': #jeżeli nie podano kodu, zwróć pierwszy wynik
            geomWkt = w['results']["1"]['geometry_wkt'] #weź pierwszy wynik z odpowiedzi serwera
            return geomWkt
        else:
            for adr in results.values():
                if adr['code'] == kod:
                    return adr['geometry_wkt']
            return None
    except KeyError:
        print(w)
        return (str(w),0)

if __name__ == '__main__':
    g = geocode(miasto='Słupno', ulica='Lipowa', numer='4', kod='09-472')
    print(g)