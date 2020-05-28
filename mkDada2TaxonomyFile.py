import argparse
import sys

def main():
    """Combine two sequence and taxonomy files into one taxonomy file for dada2"""
    parser = argparse.ArgumentParser(description='Combine a sequence and taxonomic type files into one taxonomy file for dada2')
    parser.add_argument("-seqs", help="file path to the sequence file", required=True)
    parser.add_argument("-taxo", help="file path to the taxonomy file", required=True)
    parser.add_argument("-o", help="name of the output file", default="output.taxo")
    parser.add_argument("-lrm", help="levels to remove", default="")
    parser.add_argument("--v", help="increase output verbosity", action="store_true")
    parser.add_argument("--verbose", help="increase output verbosity", action="store_true")
    args = parser.parse_args()
    verbose = args.verbose | args.v
    
    # making the sequence dictionnary
    seqs_dict = mk_seqs_dict(args.seqs)
    if(verbose):
        print('sequence dictionary complete; ' + str(len(seqs_dict.keys())) + ' entry')
    # making the taxonomy dictionnary
    taxo_dict = mk_taxo_dict(args.taxo, args.lrm)
    if(verbose):
        print('taxonomy dictionary complete; ' + str(len(taxo_dict.keys())) + ' entry')

    # writing the taxonomy file in dada2 format
    outputfile=open(args.o, "w")
    if(verbose):
        n = 0
    for key in seqs_dict.keys():
        outputfile.write(taxo_dict[key] + '\n' + seqs_dict[key] + '\n')
        if(verbose):
            n += 1
            if n % 1000 == 0 and n > 0:
                print(str(n) + " references merged") 
    if(verbose):
        print('output file complete')
    print(str(len(seqs_dict.keys())) + " references merged in " + args.o)

# making the sequence dictionnary
def mk_seqs_dict(seqs_file):    
    inputfile = open(seqs_file, "r")
    keys = []
    values = []
    for line in inputfile:
        if ">" in line:
            keys.append(line.strip()[1:])
        else :
            values.append(line.strip())
    seqs_dict = {}
    for i in range(len(keys)):
        seqs_dict[keys[i]] = values[i]
    return seqs_dict

# making the taxonomy dictionnary
def mk_taxo_dict(taxo_file, lrm):
    taxo_dict = {}
    # if there are levels to remove
    if(lrm != "") :
        inputfile = open(taxo_file, "r")
        first_line = next(inputfile).split("\t")
        tax_in = first_line[1].split(";")[0:-1]
        lrm = list(map(int, lrm.split()))
        levels = [*range(len(tax_in))]
        # keeps only the needed levels
        for l in lrm:
            levels.remove(int(l)-1)
        # because next() reads first line
        taxo_dict[first_line[0]] = '>'+';'.join([first_line[1].split(';')[0:-1][i] for i in levels])
        # this loop starts at second line
        for line in inputfile:
            taxo_dict[line.split("\t")[0]] = '>'+';'.join([line.split("\t")[1].split(';')[0:-1][i] for i in levels])
    # else just copy whole line
    else :
        inputfile = open(taxo_file, "r")
        for line in inputfile:    
            taxo_dict[line.split("\t")[0]] = '>'+line.split("\t")[1]
    return taxo_dict

if __name__ == "__main__" :
    main()