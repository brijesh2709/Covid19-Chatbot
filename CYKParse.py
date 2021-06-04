import Tree
import WebScraper
verbose = False


def printV(*args):
    if verbose:
        print(*args)


def CYKParse(words, grammar):
    T = {}
    P = {}

    def getP(X, i, k):
        key = str(X) + '/' + str(i) + '/' + str(k)
        if key in P:
            return P[key]
        else:
            return 0

    for i in range(len(words)):
        for X, p in getGrammarLexicalRules(grammar, words[i]):
            P[X + '/' + str(i) + '/' + str(i)] = p
            T[X + '/' + str(i) + '/' + str(i)] = Tree.Tree(X, None, None, lexiconItem=words[i])
    printV('P:', P)
    printV('T:', [str(t) + ':' + str(T[t]) for t in T])
    for i, j, k in subspans(len(words)):
        for X, Y, Z, p in getGrammarSyntaxRules(grammar):
            PYZ = getP(Y, i, j) * getP(Z, j + 1, k) * p
            if PYZ > getP(X, i, k):
                P[X + '/' + str(i) + '/' + str(k)] = PYZ
                T[X + '/' + str(i) + '/' + str(k)] = Tree.Tree(X, T[Y + '/' + str(i) + '/' + str(j)],
                                                               T[Z + '/' + str(j + 1) + '/' + str(k)])
    added = True
    while added:
        added = False
        for X, Y, p in getGrammarSyntaxRules2(grammar):
            PYZ = p * getP(Y, i, j)
            if PYZ > getP(X, i, k):
                P[X + '/' + str(i) + '/' + str(k)] = PYZ
                T[X + '/' + str(i) + '/' + str(k - 1)] = T[Y + '/' + str(i) + '/' + str(j)]
                added = True

    printV('T:', [str(t) + ':' + str(T[t]) for t in T])
    return T, P

def subspans(N):
    for length in range(2, N + 1):
        for i in range(N + 1 - length):
            k = i + length - 1
            for j in range(i, k):
                yield i, j, k

def getGrammarLexicalRules(grammar, word):
    for rule in grammar['lexicon']:
        if rule[1] == word:
            yield rule[0], rule[2]


def getGrammarSyntaxRules(grammar):
    rulelist = []
    for rule in grammar['syntax']:
        if len(rule) == 3:
            yield rule[0], rule[1], None, rule[2]
        else:
            yield rule[0], rule[1], rule[2], rule[3]


def getGrammarSyntaxRules2(grammar):
    rulelist1 = []
    for rule in grammar['syntax']:
        if len(rule) == 3:
            yield rule[0], rule[1], rule[2]

def countryNamesForLexicons():
    countryLexiconList = []
    for i in WebScraper.data.get_all_country_names():
        addLexiconList = []
        addLexiconList.append('Name')
        addLexiconList.append(i.lower())
        addLexiconList.append(0.8)
        countryLexiconList.append(addLexiconList)
    return countryLexiconList

def getGrammarWeather():
    synatxLexiconDict = {
        'syntax': [
            ['S', 'Greeting', 'S', 0.25],
            ['S', 'NP', 'VP', 0.25],
            ['S', 'WQuestion', 'VP', 0.25],
            ['S', 'WQuestion', 'Adverb', 0.6],
            ['S', 'WQuestion', 'Verb', 0.6],
            ['S', 'WQuestion', 'Pronoun', 0.6],
            ['S', 'WQuestion', 'Noun', 0.6],
            ['S', 'WQuestion', 'NP', 0.6],
            ['S', 'Noun', 'Preposition', 0.6],
            ['S', 'S', 'Verb', 0.6],
            ['S', 'S', 'Noun', 0.6],
            ['S', 'S', 'Preposition', 0.6],
            ['S', 'S', 'Pronoun', 0.6],
            ['S', 'S', 'AdverbPhrase', 0.6],
            ['S', 'S', 'Name', 0.6],
            ['S', 'VP', 0.25],
            ['S', 'Verb', 'Article', 0.25],
            ['S', 'S', 'Article', 0.25],
            ['S', 'S', 'Adjective', 0.25],
            ['S', 'NP', 'Verb', 0.9 * 0.45 * 0.4],
            ['S', 'NP', 'VP', 0.9 * 0.45 * 0.6],
            ['S', 'Pronoun', 'VP', 0.9 * 0.25 * 0.6],
            ['S', 'Name', 'VP', 0.9 * 0.10 * 0.6],
            ['S', 'Noun', 'VP', 0.9 * 0.10 * 0.6],
            ['S', 'NP', 'Verb', 0.9 * 0.45 * 0.4],
            ['S', 'Pronoun', 'Verb', 0.9 * 0.25 * 0.4],
            ['S', 'Name', 'Verb', 0.9 * 0.10 * 0.4],
            ['S', 'Noun', 'Verb', 0.9 * 0.10 * 0.4],
            ['S', 'S', 'Conj+S', 0.1],
            ['Conj+S', 'Conj', 'S', 1.0],

            ['VP', 'VP', 'NP', 0.6 * 0.55],
            ['VP', 'VP', 'Adjective', 0.6 * 0.1],
            ['VP', 'VP', 'PP', 0.6 * 0.2],
            ['VP', 'VP', 'Adverb', 0.6 * 0.15],
            ['VP', 'Verb', 'Adjective', 0.4 * 0.1],
            ['VP', 'Verb', 'PP', 0.4 * 0.2],
            ['VP', 'Verb', 'Adverb', 0.4 * 0.15],
            ['VP', 'Verb', 0.5],
            ['VP', 'Verb', 'NP', 0.4],
            ['VP', 'Verb', 'Name', 0.2],
            ['VP', 'Verb', 'NP+AdverbPhrase', 0.3],

            ['NP', 'Article+Adjs', 'Noun', 0.15],
            ['NP', 'Article+Adjective', 'Noun', 0.05],
            ['NP', 'NP', 'PP', 0.2],
            ['NP', 'NP', 'RelClause', 0.15],
            ['NP', 'NP', 'Conj+NP', 0.05],
            ['NP', 'NP', 'VP', 0.3],
            ['NP', 'Pronoun', 0.3],
            ['NP', 'NP', 'AdjectivePhrase', 0.4],
            ['NP', 'Name', 0.10],
            ['NP', 'Noun', 0.10],
            ['NP', 'Article', 'Noun', 0.4],
            ['NP', 'Adjective', 'Noun', 0.4],

            ['Conj+NP', 'Conj', 'NP', 1.0],
            ['Adjs', 'Adjective', 0.8],
            ['Article+Adjs', 'Article', 'Adjs', 1.0],
            ['Article+Adjective', 'Article', 'Adjective', 1.0],
            ['Adjs', 'Adjective', 'Adjs', 0.8],

            ['NP+AdverbPhrase', 'NP', 'AdverbPhrase', 0.2],
            ['NP+AdverbPhrase', 'Noun', 'AdverbPhrase', 0.2],
            ['NP+AdverbPhrase', 'Noun', 'Adverb', 0.2],
            ['NP+AdverbPhrase', 'NP', 'Adverb', 0.15],
            ['NP+AdverbPhrase', 'AdverbPhrase', 'NP', 0.05],
            ['NP+AdverbPhrase', 'AdverbPhrase', 'Noun', 0.05],
            ['NP+AdverbPhrase', 'Adverb', 'Noun', 0.05],
            ['NP+AdverbPhrase', 'Adverb', 'NP+AdverbPhrase', 0.05],
            ['NP+AdverbPhrase', 'Adverb', 'NP', 0.05],

            ['PP', 'Prep', 'NP', 0.65],
            ['PP', 'Prep', 'Pronoun', 0.2],
            ['PP', 'Prep', 'Name', 0.1],
            ['PP', 'Prep', 'Noun', 0.05],

            ['RelClause', 'RelPro', 'VP', 0.6],
            ['RelClause', 'RelPro', 'Verb', 0.4],

            ['AdverbPhrase', 'Preposition', 'NP', 0.2],
            ['AdverbPhrase', 'Preposition', 'Name', 0.2],
            ['AdverbPhrase', 'Adverb', 'AdverbPhrase', 0.2],
            ['AdverbPhrase', 'AdverbPhrase', 'Adverb', 0.4],
        ],

        'lexicon': [
            ['Greeting', 'hi', 0.5],
            ['Greeting', 'hello', 0.5],
            ['WQuestion', 'what', 0.5],
            ['WQuestion', 'when', 0.25],
            ['WQuestion', 'which', 0.25],
            ['WQuestion', 'will', 0.25],
            ['WQuestion', 'how', 0.25],
            ['WQuestion', 'can', 0.25],
            ['Verb', 'be', 0.5],
            ['Verb', 'am', 0.5],
            ['Verb', 'have', 0.5],
            ['Verb', 'get', 0.5],
            ['Verb', 'is', 0.5],
            ['Verb', 'are', 0.5],
            ['Name', 'peter', 0.1],
            ['Name', 'sue', 0.1],
            ['Name', 'irvine', 0.8],
            ['Name', 'tustin', 0.8],
            ['Name', 'world', 0.8],
            ['Name', 'pasadena', 0.8],
            ['Pronoun', 'i', 1.0],
            ['Pronoun', 'many', 1.0],
            ['Pronoun', 'this', 1.0],
            ['Noun', 'hotter', 0.2],
            ['Noun', 'number', 0.2],
            ['Noun', 'count', 0.2],
            ['Noun', 'cases', 0.2],
            ['Noun', 'deaths', 0.2],
            ['Noun', 'tests', 0.2],
            ['Noun', 'population', 0.2],
            ['Noun', 'people', 0.2],
            ['Noun', 'recovered', 0.2],
            ['Noun', 'pandemic', 0.2],
            ['Noun', 'man', 0.2],
            ['Noun', 'name', 0.2],
            ['Noun', 'coronavirus', 0.2],
            ['Noun', 'data', 0.2],
            ['Noun', 'statistics', 0.2],
            ['Noun', 'covid', 0.2],
            ['Noun', 'covid19', 0.2],
            ['Noun', 'temperature', 0.6],
            ['Article', 'the', 0.7],
            ['Article', 'a', 0.3],
            ['Adjective', 'my', 1.0],
            ['Adjective', 'active', 1.0],
            ['Adjective', 'total', 1.0],
            ['Adverb', 'now', 0.4],
            ['Adverb', 'today', 0.3],
            ['Adverb', 'there', 0.3],
            ['Adverb', 'around', 0.3],
            ['Adverb', 'tomorrow', 0.3],
            ['Adverb', 'yesterday', 0.3],
            ['Preposition', 'with', 0.5],
            ['Preposition', 'in', 0.5],
            ['Preposition', 'than', 0.5],
            ['Preposition', 'of', 0.5],
            ['Preposition', 'from', 0.5],
            ['Preposition', 'about', 0.5],
            ['Preposition', 'on', 0.5],
            ['Preposition', 'number', 0.5],


        ]
    }

    for i in countryNamesForLexicons():
        synatxLexiconDict['lexicon'].append(i)
    return synatxLexiconDict


# Unit testing code
if __name__ == '__main__':
    verbose = True
    # CYKParse(['what', 'is', 'the', 'cases', 'in', 'india'], getGrammarWeather())
    # CYKParse(['statistics', 'on', 'india'], getGrammarWeather())
# CYKParse(['the', 'old', 'man', 'the', 'boat'], getGrammarGardenPath())
# CYKParse(['what', 'is', 'the', 'total', 'covid', 'cases'], getGrammarWeather())
