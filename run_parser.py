from brand_parser import BrandNameParser, BurberryParser, KenzoParser


###START PARSER##
output_directory_path = 'parser-output'


directory_path = 'brand_name'

brand_name_parser = BrandNameParser(output_directory_path)
#brand_name_parser.parse_directory(directory_path)


# BurberryParser RUN
directory_path = 'burberry'

burberry_parser = BurberryParser(output_directory_path)
#burberry_parser.parse_directory(directory_path)

#KenzoParser RUN
directory_path = 'kenzo'

kenzo_parser = KenzoParser(output_directory_path)
kenzo_parser.parse_directory(directory_path)



