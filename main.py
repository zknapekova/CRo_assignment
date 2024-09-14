from functions import delete_rows, parse_xml, parse_arguments, validate_arguments
import pandas as pd

def main():
    #df = pd.read_csv('data_cleanup.tsv', sep='\t')
    #print(delete_rows(df, id_col='ObjectID', check_na_col='Name'))

    args = parse_arguments()
    validate_arguments(args)
    parse_xml(args.source, args.out_type, args.output)


if __name__ == "__main__":
    main()


