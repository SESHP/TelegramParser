from ParserSearch import ParserSearching

parser = ParserSearching('/Users/buzeoff/Downloads/chromedriver-mac-arm64/chromedriver')
input_names = input("Введите имена для поиска: ")
results = parser.run(input_names)
print(results)