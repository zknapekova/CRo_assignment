from functions import *
import pandas as pd

def main():

    #df = pd.read_csv('data_cleanup.tsv', sep='\t')
    #print(delete_rows(df, id_col='ObjectID', check_na_col='Name'))

    args = parse_arguments()
    if args.command == 'parse_file':
        validate_arguments_parse_file(args)
        parse_xml(args.source, output_type=args.out_type, output_file=args.output)
    elif args.command == 'search_and_parse':
        files_to_parse = find_xml_files(directory=args.source_dir, search_sub=args.search_sub, regex=args.regex)
        for file in files_to_parse:
            parse_xml(file, output_type=args.out_type, output_dir=args.output_dir)


if __name__ == "__main__":
    main()


