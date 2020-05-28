import argparse
import sys

#example usage from terminal :
#python3 ./mkDada2TaxonomyFile.py -s "./sequences.fasta" -ssep '|' -t "./tax.txt"  -o "./dada2tax.fasta" --v 

def main():
    parser = argparse.ArgumentParser(description='Combine a sequence and taxonomic type files into one taxonomy file in dada2 or standard format')
    parser.add_argument("-s", help="file path to the sequence file", required=True)
    parser.add_argument("-ssep", help="separator for the id line of the sequence file",  default=False)
    parser.add_argument("-t", help="file path to the taxonomy file", required=True)
    parser.add_argument("-o", help="file path to the output file", default="output.taxo")
    parser.add_argument("-lrm", help="taxonomic levels to remove (optional)", default="")
    parser.add_argument("--v", help="increase output verbosity (optional)", action="store_true")
    parser.add_argument("--verbose", help="increase output verbosity (optional)", action="store_true")
    parser.add_argument("--standard", help="taxonomic format; if this argument isn't added it will output in dada2 format (optional);", action="store_true", default=False)
    args = parser.parse_args()
    verbose = args.verbose | args.v
    
    # making the sequence dictionnary
    seqs_dict = mk_seqs_dict(args.s, args.ssep, args.standard)
    if(verbose):
        print('sequence dictionary complete; ' + str(len(seqs_dict.keys())) + ' entry')
    # making the taxonomy dictionnary
    taxo_dict = mk_taxo_dict(args.t, args.lrm)
    if(verbose):
        print('taxonomy dictionary complete; ' + str(len(taxo_dict.keys())) + ' entry')

    # writing the taxonomy file in dada2 format
    outputfile=open(args.o, "w")
    if(verbose):
        n = 0
    for key in seqs_dict.keys():
        if(args.standard):
            tax_line = '>' + '|'.join([taxo_dict[key][-1], key, seqs_dict[key]['name'], 'refs', ';'.join(taxo_dict[key])]) +  '\n'
        else :
            tax_line = '>' + ';'.join(taxo_dict[key]) + '\n'
        seq_line = seqs_dict[key]['value'] +  '\n'
        outputfile.write(tax_line + seq_line)
        if(verbose):
            n += 1
            if n % 1000 == 0 and n > 0:
                print(str(n) + " references merged") 
    if(verbose):
        print('output file complete')
    print(str(len(seqs_dict.keys())) + " references merged in " + args.o)

# making the sequence dictionnary
def mk_seqs_dict(seqs_file, seqs_sep, std):    
    inputfile = open(seqs_file, "r")
    keys = []
    values = []
    if(std):
        names = []
    for line in inputfile:
        if ">" in line:
            if(seqs_sep):
                line = line.strip().split(seqs_sep)
                key = line[0][1:]
                keys.append(key)
                if(std):
                    names.append(line[1])
            else :
                key = line.strip()[1:]
                keys.append(key)
                names.append(key)
        else :
            values.append(line.strip())
    seqs_dict = {}
    for i in range(len(keys)):
        seqs_dict[keys[i]] = {'value' : values[i]}
        if(std) : 
            seqs_dict[keys[i]]['name'] = names[i]
    return seqs_dict

# making the taxonomy dictionnary
def mk_taxo_dict(taxo_file, lrm):
    taxo_dict = {}
    inputfile = open(taxo_file, "r")
    lrm = list(map(int, lrm.split()))
    for line in inputfile:
        line = line.strip().split("\t")
        key = line[0]
        value = line[1].split(";")
        # if there are levels to remove
        if(lrm != ""):
            # removes them from value
            for l in lrm:
                value.remove(value[int(l)-1])
        taxo_dict[key] = value
    return taxo_dict

if __name__ == "__main__" :
    main()