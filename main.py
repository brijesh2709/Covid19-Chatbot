
import CYKParse
import WebScraper
import re
import matplotlib.pyplot as plt

API_KEY = "tUsxS-TrJ2pB"
PROJECT_TOKEN = "tTTNTwG7H25d"
data = WebScraper.Data(API_KEY, PROJECT_TOKEN)

requestTotalInfo = {
    'name': '',
    'totWord': '',
    'cdr': '',
    'location': ''
}

haveGreeted = False


# Given the collection of parse trees returned by CYKParse, this function
# returns the one corresponding to the complete sentence.
def getSentenceParse(T):
    sentenceTrees = {k: v for k, v in T.items() if k.startswith('S/0')}
    completeSentenceTree = max(sentenceTrees.keys())
    return T[completeSentenceTree]


# Processes the leaves of the parse tree to pull out the user's request.
def updateRequestInfo(Tr):
    global requestTotalInfo
    requestTotalInfo['totWord'] = ''
    lookingForName = False
    lookingForLocation = False
    for leaf in Tr.getLeaves():
        if lookingForLocation and leaf[0] == 'Name':
            requestTotalInfo['location'] = leaf[1]
        if leaf[0] == 'Preposition' and leaf[1] in ['in', 'on', 'about']:
            lookingForLocation = True
        elif leaf[0] == 'Article' and leaf[1] == 'the':
            lookingForLocation = True
        else:
            lookingForLocation = False

        if leaf[0] == 'Noun' and leaf[1] == 'cases':
            requestTotalInfo['cdr'] = leaf[1]
        elif leaf[0] == 'Noun' and leaf[1] == 'deaths':
            requestTotalInfo['cdr'] = leaf[1]
        elif leaf[0] == 'Noun' and leaf[1] == 'recovered':
            requestTotalInfo['cdr'] = leaf[1]
        elif leaf[0] == 'Noun' and leaf[1] == 'tests':
            requestTotalInfo['cdr'] = leaf[1]
        elif leaf[0] == 'Noun' and leaf[1] == 'population':
            requestTotalInfo['cdr'] = leaf[1]

        if leaf[0] == 'Adjective' and leaf[1] == 'total':
            requestTotalInfo['totWord'] = leaf[1]

        if (leaf[0] == 'Noun' and leaf[1] == 'name') or (leaf[0] == 'Pronoun' and leaf[1] == 'i'):
            lookingForName = True
        if lookingForName and leaf[0] == 'Name':
            requestTotalInfo['name'] = leaf[1]


def getTotalInfo(location, cdr_status, totalKeyWord):
    if cdr_status == 'cases':
        update_cdr_status = cdr_status[:4]
        TOTAL_PATTERNS = {
            re.compile(f"[\w\s]+ {totalKeyWord} [\w\s]+ \\b{update_cdr_status}\\w"): data.get_total_cases,
            re.compile(f"[\w\s]+ {totalKeyWord} [\w\s]+ \\b{update_cdr_status}\\w [\w\s]+{location}"): data.get_total_cases,
            re.compile(f"[\w\s]+ {totalKeyWord} \\b{update_cdr_status}\\w"): data.get_total_cases,
            re.compile(f"{totalKeyWord} \\b{update_cdr_status}\\w [\w\s]+"): data.get_total_cases
        }
        for pattern, func in TOTAL_PATTERNS.items():
            result = func()
            break

    elif cdr_status == 'deaths':
        update_cdr_status = cdr_status[:4]

        TOTAL_PATTERNS = {
            re.compile(f"[\w\s]+ {totalKeyWord} [\w\s]+ \\b{update_cdr_status}\\w"): data.get_total_deaths,
            re.compile(f"[\w\s]+ {totalKeyWord} [\w\s]+ \\b{update_cdr_status}\\w [\w\s]+{location}"): data.get_total_deaths,
            re.compile(f"[\w\s]+ {totalKeyWord} \\b{update_cdr_status}\\w"): data.get_total_deaths
        }
        for pattern, func in TOTAL_PATTERNS.items():
            result = func()
            break

    elif cdr_status == 'recovered':
        update_cdr_status = cdr_status[:4]

        TOTAL_PATTERNS = {
            re.compile(f"[\w\s]+ {totalKeyWord} [\w\s]+ \\b{update_cdr_status}\\w"): data.get_total_recoverd,
            re.compile(f"[\w\s]+ {totalKeyWord} [\w\s]+ \\b{update_cdr_status}\\w [\w\s]+{location}"): data.get_total_recoverd,
            re.compile(f"[\w\s]+ {totalKeyWord} \\b{update_cdr_status}\\w"): data.get_total_recoverd
        }
        for pattern, func in TOTAL_PATTERNS.items():
            result = func()
            break

    return result

def getCountryInfo(location, cdr_status, totalKeyWord):
    if cdr_status == 'cases':
        update_cdr_status = cdr_status[:4]
        COUNTRY_PATTERNS = {
            re.compile(f"\\b{update_cdr_status}\\w {location} [\w\s]+"): data.get_specific_country_data(location)['total_cases'],
            re.compile(f"\\b{update_cdr_status}\\w [\w\s]+ {location}"): data.get_specific_country_data(location)['total_cases'],
            re.compile(f"[\w\s]+ \\b{update_cdr_status}\\w {location}"): data.get_specific_country_data(location)['total_cases'],
            re.compile(f"[\w\s]+ \\b{update_cdr_status}\\w [\w\s]+ {location}"): data.get_specific_country_data(location)['total_cases'],
        }
        for pattern, func in COUNTRY_PATTERNS.items():
            result = func
            break

    elif cdr_status == 'deaths':
        update_cdr_status = cdr_status[:4]

        COUNTRY_PATTERNS = {
            re.compile(f"\\b{update_cdr_status}\\w {location} [\w\s]+"): data.get_specific_country_data(location)['total_deaths'],
            re.compile(f"\\b{update_cdr_status}\\w [\w\s]+ {location}"): data.get_specific_country_data(location)['total_deaths'],
            re.compile(f"[\w\s]+ \\b{update_cdr_status}\\w {location}"): data.get_specific_country_data(location)['total_deaths'],
            re.compile(f"[\w\s]+ \\b{update_cdr_status}\\w [\w\s]+ {location}"): data.get_specific_country_data(location)['total_deaths'],
        }
        for pattern, func in COUNTRY_PATTERNS.items():
            result = func
            break

    elif cdr_status == 'recovered':
        update_cdr_status = cdr_status[:4]

        COUNTRY_PATTERNS = {
            re.compile(f"\\b{update_cdr_status}\\w {location} [\w\s]+"): data.get_specific_country_data(location)['total_recovered'],
            re.compile(f"\\b{update_cdr_status}\\w [\w\s]+ {location}"): data.get_specific_country_data(location)['total_recovered'],
            re.compile(f"[\w\s]+ \\b{update_cdr_status}\\w {location}"): data.get_specific_country_data(location)['total_recovered'],
            re.compile(f"[\w\s]+ \\b{update_cdr_status}\\w [\w\s]+ {location}"): data.get_specific_country_data(location)['total_recovered'],
        }
        for pattern, func in COUNTRY_PATTERNS.items():
            result = func
            break

    elif cdr_status == 'tests':
        update_cdr_status = cdr_status[:4]

        COUNTRY_PATTERNS = {
            re.compile(f"\\b{update_cdr_status}\\w {location} [\w\s]+"): data.get_specific_country_data(location)['total_tests'],
            re.compile(f"\\b{update_cdr_status}\\w [\w\s]+ {location}"): data.get_specific_country_data(location)['total_tests'],
            re.compile(f"[\w\s]+ \\b{update_cdr_status}\\w {location}"): data.get_specific_country_data(location)['total_tests'],
            re.compile(f"[\w\s]+ \\b{update_cdr_status}\\w [\w\s]+ {location}"): data.get_specific_country_data(location)['total_tests'],
        }
        for pattern, func in COUNTRY_PATTERNS.items():
            result = func
            break

    elif cdr_status == 'population':
        update_cdr_status = cdr_status[:4]

        COUNTRY_PATTERNS = {
            re.compile(f"\\b{update_cdr_status}\\w {location} [\w\s]+"): data.get_specific_country_data(location)['total_population'],
            re.compile(f"\\b{update_cdr_status}\\w [\w\s]+ {location}"): data.get_specific_country_data(location)['total_population'],
            re.compile(f"[\w\s]+ \\b{update_cdr_status}\\w {location}"): data.get_specific_country_data(location)['total_population'],
            re.compile(f"[\w\s]+ \\b{update_cdr_status}\\w [\w\s]+ {location}"): data.get_specific_country_data(location)['total_population'],
        }
        for pattern, func in COUNTRY_PATTERNS.items():
            result = func
            break

    return result

def plot_country_data(location):
    fig = plt.figure()
    ax = fig.add_axes([0, 0, 1, 1])
    status = ['Ig', 'Cases', 'Deaths', 'Recovered', 'Tests', 'Population']
    count = [data.get_zero_value(),
             data.get_specific_country_data(location)['total_cases'],
             data.get_specific_country_data(location)['total_deaths'],
             data.get_specific_country_data(location)['total_recovered'],
             data.get_specific_country_data(location)['total_tests'],
             data.get_specific_country_data(location)['total_population']
             ]
    ax.bar(status, count, color = 'b')
    plt.xlabel('Population')
    plt.show()

def reply():
    global requestTotalInfo
    global haveGreeted
    if not haveGreeted and requestTotalInfo['name'] != '':
        print("Hello", requestTotalInfo['name'].capitalize() + '.' + " How may I assist you?")
        haveGreeted = True
        return
    cdrStatus = 'cases'  # the default
    if requestTotalInfo['cdr'] != '':
        cdrStatus = requestTotalInfo['cdr']
    salutation = ''
    if requestTotalInfo['name'] != '':
        salutation = requestTotalInfo['name'] + ', '

    if requestTotalInfo['location'] in WebScraper.data.get_all_country_names():
        if requestTotalInfo['cdr'] in ['cases', 'deaths', 'recovered', 'tests', 'population']:
            print(salutation.capitalize() + 'the ' + ' ' + requestTotalInfo['cdr'] + ' is ' +
                  getCountryInfo(requestTotalInfo['location'], requestTotalInfo['cdr'], requestTotalInfo['totWord']) + '.')

        else:
            plot_country_data(requestTotalInfo['location'])
    else:
        print(salutation.capitalize() + 'the ' + requestTotalInfo['totWord'] + ' ' +
              requestTotalInfo['cdr'] + ' is ' + getTotalInfo(requestTotalInfo['location'], requestTotalInfo['cdr'],
                                                              requestTotalInfo['totWord']) + '.')


def main():
    global requestTotalInfo
    print(" Hello. I am Veronica. I am your up-to-date COVID tracker. What is your name?")
    while True:
        getInp = input(">> ")
        getInp = getInp.lower()
        getInp_list = getInp.split(" ")
        try:
            if getInp_list[0] in ['bye', 'Thanks', 'thanks', 'Bye']:
                print("Stay Safe and Wear mask. Bye !")
                break
            elif getInp == "what can i ask for":
                print("1) Total cases, deaths, and recovered in the world")
                print("2) Cases, deaths, recovered, tests, and population in any of the country")
                print("3) Statistics on each country(Can be Downloaded as PNG file)")
            else:
                T, P = CYKParse.CYKParse(getInp_list, CYKParse.getGrammarWeather())
                sentenceTree = getSentenceParse(T)
                updateRequestInfo(sentenceTree)
                reply()
        except:
            if requestTotalInfo['location'] == '':
                print('Sorry, I did not understand')
            else:
                print(f'Sorry, I did not understand. Irvine is not a country')


main()