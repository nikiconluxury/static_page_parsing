from brand_parser import BrandNameParser


###START PARSER##
output_directory_path = 'parser-output'
directory_path = 'brand_name'

brand_name_parser = BrandNameParser(output_directory_path)
brand_name_parser.parse_directory(directory_path)