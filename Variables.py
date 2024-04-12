import os

file_collection2 = ['D:/NaUKMA/year 2/інфопошук/A_Sea_Change-Veronica_Henry.txt',
                    'D:/NaUKMA/year 2/інфопошук/Barchester_Towers-Anthony_Trollope.txt',
                    'D:/NaUKMA/year 2/інфопошук/Catch_Me_If_You_Can-Frank_W_Abagnale.txt',
                    'D:/NaUKMA/year 2/інфопошук/Murder_in_the_Fog-Dominic_Butler.txt',
                    'D:/NaUKMA/year 2/інфопошук/Some book part 2.txt',
                    'D:/NaUKMA/year 2/інфопошук/Some book.txt',
                    'D:/NaUKMA/year 2/інфопошук/The_Accidental_Tourist-Anne_Tyler.txt',
                    'D:/NaUKMA/year 2/інфопошук/The_Bride_Price-Buchi_Emecheta.txt',
                    'D:/NaUKMA/year 2/інфопошук/The_Bridges_of_Madison_County-Robert_James_Waller.txt',
                    'D:/NaUKMA/year 2/інфопошук/The_Ghost_and_the_Document_Reviewer-Gayle_Tiller.txt',
                    'D:/NaUKMA/year 2/інфопошук/bible.txt',
                    'D:/NaUKMA/year 2/інфопошук/quran.txt',
                    'D:/NaUKMA/year 2/інфопошук/googlebooks-eng-all-2gram-20120701-dw',
                    'D:/NaUKMA/year 2/інфопошук/The Poetical Works of John Milton.txt',
                    'D:/NaUKMA/year 2/інфопошук/googlebooks-eng-us-all-5gram-20120701-kc',
                    'D:/NaUKMA/year 2/інфопошук/googlebooks-eng-gb-all-2gram-20120701-am']

file_collection = file_collection2.copy()
file_collection.remove('D:/NaUKMA/year 2/інфопошук/googlebooks-eng-gb-all-2gram-20120701-am')
file_collection.remove('D:/NaUKMA/year 2/інфопошук/googlebooks-eng-all-2gram-20120701-dw')
file_collection.remove('D:/NaUKMA/year 2/інфопошук/googlebooks-eng-us-all-5gram-20120701-kc')

path = 'D:/NaUKMA/year 2/інфопошук/books1/epubtxt'
big_collection = []

for root, dirs, files in os.walk(path):
    for file in files:
        big_collection.append(os.path.join(root, file))


path = 'D:/NaUKMA/year 2/інфопошук/cranfield collection/cranfield unpacked'
cranfield_collection = []

for root, dirs, files in os.walk(path):
    for file in files:
        cranfield_collection.append(os.path.join(root, file))


small_collection = ['D:/NaUKMA/year 2/інфопошук/hello.txt',
                    'D:/NaUKMA/year 2/інфопошук/name.txt',
                    'D:/NaUKMA/year 2/інфопошук/tea.txt',
                    'D:/NaUKMA/year 2/інфопошук/one more.txt']

collection = ["D:/NaUKMA/year 2/інфопошук/Eve's Diary, By Mark Twain.html",
              "D:/NaUKMA/year 2/інфопошук/Everyman with other interludes.html"]

fb2_collection = ['D:/NaUKMA/year 2/інфопошук/The Mystery of Marie Roget.fb2',
                  'D:/NaUKMA/year 2/інфопошук/The Murders in the Rue Morgue.fb2',
                  'D:/NaUKMA/year 2/інфопошук/Madame_Bovary-Gustave_Flaubert.fb2']
