"""
## Zemberek: Noisy Text Normalization Example
# Documentation: https://bit.ly/2WkUVVF

## Zemberek: Turkish Spell Checking Example
# Documentation: https://bit.ly/2pYWVqC
"""

from os.path import join
from typing import List
from jpype import JClass, JString, getDefaultJVMPath, shutdownJVM, startJVM
import pandas as pd
import re
from nltk.corpus import stopwords

df = pd.read_csv("magaza_yorumlari.csv", encoding = "utf-16")

gorusler = df['Görüş']
durumlar = df["Durum"]

gorusler_temiz = []
for text in gorusler:
    text = str(text)
    x = text.lower()
    x = re.sub(r'https?:\/\/.*[\r\n]*', '', x, flags=re.MULTILINE)
    x = re.sub(r'\<a href', ' ', x)
    x = re.sub(r'&amp;', '', x)
    x = re.sub(r'<br />', ' ', x)
    x = re.sub(r"^\s+|\s+$", "", x)
    x = x.split()
    x = ' '.join(x)
    gorusler_temiz.append(x)

gurultusuz_gorusler = []
gorusler_son = []

if __name__ == '__main__':

    ZEMBEREK_PATH: str = join('..', '..', 'bin', 'zemberek-full.jar')

    startJVM(getDefaultJVMPath(),'-ea',f'-Djava.class.path={ZEMBEREK_PATH}',convertStrings=False)

    TurkishMorphology: JClass = JClass('zemberek.morphology.TurkishMorphology')
    TurkishSentenceNormalizer: JClass = JClass('zemberek.normalization.TurkishSentenceNormalizer')

    Paths: JClass = JClass('java.nio.file.Paths')

    normalizer = TurkishSentenceNormalizer(TurkishMorphology.createWithDefaults(),Paths.get(join('..', '..', 'data', 'normalization')),Paths.get(join('..', '..', 'data', 'lm', 'lm.2gram.slm')))

    for i, example in enumerate(gorusler_temiz):
        gurultusuz_gorusler.append([str(normalizer.normalize(JString(example)))])

    TurkishMorphology: JClass = JClass('zemberek.morphology.TurkishMorphology')
    TurkishSpellChecker: JClass = JClass('zemberek.normalization.TurkishSpellChecker')

    morphology: TurkishMorphology = TurkishMorphology.createWithDefaults()

    spell_checker: TurkishSpellChecker = TurkishSpellChecker(morphology)
    for i in gurultusuz_gorusler:
        words: List[str] = i[0].split()

        for word in words:
            suggestions = spell_checker.suggestForWord(JString(word))
            if suggestions:
                for suggestion in suggestions:
                    print(f' | {suggestion}')

        for i, word in enumerate(words):
            if spell_checker.suggestForWord(JString(word)):
                if not spell_checker.check(JString(word)):
                    words[i] = str(spell_checker.suggestForWord(JString(word))[0])

        gorusler_son.append(' '.join(words))
    shutdownJVM()

gorusler_temiz = []
etkisizler = list(stopwords.words('Turkish'))
for text in gorusler_son:
    text = str(text)
    x = text.lower()
    x = re.sub(r'\W', ' ', str(x))
    x = re.sub(r'[_"\-;%()|+&=*%.,!?:#$@\[\]/]', ' ', x)
    x = re.sub(r'\'', ' ', x)
    x = re.sub('\s{2,}', ' ', x)
    x = re.sub(r'\s+[a-zA-Z]\s+', ' ', x)
    x = re.sub(r'\^[a-zA-Z]\s+', ' ', x)
    x = re.sub(r'\s+', ' ', x, flags=re.I)
    x = re.sub(r'^b\s+', '', x)
    x = x.split()
    x = [word for word in x if word not in etkisizler]
    x = ' '.join(x)
    gorusler_temiz.append(x)

dosya = set(zip(gorusler_temiz, durumlar))
df = pd.DataFrame(dosya, columns=['Görüş','Durum'])
df.to_csv('magaza_yorumlari_oo.csv', index = False, encoding = 'utf-16')
